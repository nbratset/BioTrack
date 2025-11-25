import os
import sys
sys.path.append("src")

import numpy as np
import pandas as pd
from diversity import compute_alpha, compute_beta
from ordination import run_pcoa
from taxonomy_plot import barplot_taxa_facet_fill
import matplotlib.pyplot as plt
import seaborn as sns

#Save results
OUTDIR = "results"
os.makedirs(OUTDIR, exist_ok=True)
            
# Load data
otu = pd.read_csv("input_data/otu.csv", index_col=0)      # samples as rows, OTUs as columns
tax = pd.read_csv("input_data/tax.csv", index_col=0)      # ASV/OTU as index, taxonomy strings as values
metadata = pd.read_csv("input_data/combined_metadata.csv", index_col=0)

# Visualization of top 10 species
taxonomy_series = tax.apply(lambda row: ";".join(row.values.astype(str)), axis=1)
taxonomy_series.index = tax.index

otu_clean = otu.drop(columns=["SortKey"], errors="ignore")

barplot_taxa_facet_fill(
    otu_table=otu_clean,
    taxonomy_series=taxonomy_series,
    metadata=metadata,
    level="Genus",
    top_n=10,
    out_file=f"{OUTDIR}/top10_taxa_by_condition.png"
)


# Beta diversity analysiss
beta = compute_beta(otu)
coords, var_exp = run_pcoa(beta)
coords = coords.join(metadata[["Condition", "Location"]])

##PCoA1 vs PCoA2
plt.figure(figsize=(15,10))
sns.scatterplot(
    x="PC1",
    y="PC2",
    data=coords[coords["Condition"] != "Patient"],
    s=100,
    hue="Condition",
    alpha=0.7,
    edgecolor="k",
    palette="tab10",
    style="Location",    
    legend=True
)
sns.scatterplot(
    x="PC1",
    y="PC2",
    data=coords[coords["Condition"] == "Patient"],
    s=150,
    color="red",
    marker="X",               
    edgecolor="k",
    label="Patient"
)
plt.xlabel(f"PCoA1 ({var_exp[0]*100:.1f}%)")
plt.ylabel(f"PCoA2 ({var_exp[1]*100:.1f}%)")
plt.title("PCoA Plot (Bray-Curtis)")
plt.legend(bbox_to_anchor=(1.05,1), loc="upper left", title="Condition")
plt.tight_layout()
plt.savefig(f"{OUTDIR}/pcoa_plot.png", dpi=300)
plt.close()


#Alpha diversity
alpha_df = compute_alpha(otu)
alpha_df
alpha_df = alpha_df.join(metadata[["Condition", "Location"]])
alpha_df.to_csv(f"{OUTDIR}/alpha_diversity.csv")

plt.figure(figsize=(10,6))
g = sns.catplot(
    data=alpha_df,
    x="Condition",
    y="Observed",
    col="Location",
    kind="box",
    height=4,
    aspect=1,
    showfliers=False,     
    boxprops={'alpha':0.7},
    col_wrap=3
)
for ax, loc in zip(g.axes.flat, alpha_df["Location"].unique()):
    df_sub = alpha_df[alpha_df["Location"] == loc]
    sns.stripplot(
        x="Condition",
        y="Observed",
        data=df_sub,
        color="black",
        size=6,
        jitter=True,
        alpha=0.8,
        ax=ax
    )
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
g.set_axis_labels("Condition", "Observed Alpha Diversity")
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle("Alpha Diversity (Richness)", fontsize=16)
plt.tight_layout()
plt.savefig(f"{OUTDIR}/alpha_diversity_plot_obs.png", dpi=300)
plt.close()


plt.figure(figsize=(10,6))
g = sns.catplot(
    data=alpha_df,
    x="Condition",
    y="Shannon",
    col="Location",
    kind="box",
    height=4,
    aspect=1,
    showfliers=False,     
    boxprops={'alpha':0.7},
    col_wrap=3
)
for ax, loc in zip(g.axes.flat, alpha_df["Location"].unique()):
    df_sub = alpha_df[alpha_df["Location"] == loc]
    sns.stripplot(
        x="Condition",
        y="Shannon",
        data=df_sub,
        color="black",
        size=6,
        jitter=True,
        alpha=0.8,
        ax=ax
    )
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
g.set_axis_labels("Condition", "Observed Alpha Diversity")
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle("Alpha Diversity (Shannon)", fontsize=16)
plt.tight_layout()
plt.savefig(f"{OUTDIR}/alpha_diversity_plot_shannon.png", dpi=300)
plt.close()





