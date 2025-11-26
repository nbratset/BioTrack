import os
import sys
sys.path.append("src")

import numpy as np
import pandas as pd
from diversity import compute_alpha, compute_beta
from ordination import run_pcoa
from taxonomy_plot import barplot_taxa_facet_fill
from randomforest import run_rf_multiclass
import matplotlib.pyplot as plt
import seaborn as sns
from skbio.stats.composition import ancom
import argparse

# --- argparse ---
parser = argparse.ArgumentParser()
parser.add_argument("--otu", required=True)
parser.add_argument("--meta", required=True)
args = parser.parse_args()

# Load data
otu = pd.read_csv(args.otu, index_col=0)
metadata = pd.read_csv(args.meta, index_col=0)
tax = pd.read_csv("input_data/tax.csv", index_col=0)      

#Save results
OUTDIR = "results"
os.makedirs(OUTDIR, exist_ok=True)

#QC filtering
min_abundance = 0.001
min_samples = 5
otu =  otu.loc[:, (otu > min_abundance).sum(axis=0) >= min_samples] 

# Visualization of top 10 species
taxonomy_series = tax.apply(lambda row: ";".join(row.values.astype(str)), axis=1)
taxonomy_series.index = tax.index

barplot_taxa_facet_fill(
    otu_table=otu,
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
coords.to_csv(f"{OUTDIR}/beta_diversity_coords.csv")

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


plt.figure(figsize=(12,8))
sns.boxplot(
    x="PC1",
    y="Condition",
    data=coords,
    palette="tab10"
)
plt.xlabel(f"PCoA1 ({var_exp[0]*100:.1f}%)")
plt.title("PCoA1 Boxplot (Bray-Curtis)")
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.tight_layout()
plt.savefig(f"{OUTDIR}/pcoa1_boxplot.png", dpi=300)
plt.close()


plt.figure(figsize=(12,8))
sns.boxplot(
    x="PC2",
    y="Condition",
    data=coords,
    palette="tab10"
)
plt.xlabel(f"PCoA2 ({var_exp[1]*100:.1f}%)")
plt.title("PCoA2 Boxplot (Bray-Curtis)")
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.tight_layout()
plt.savefig(f"{OUTDIR}/pcoa2_boxplot.png", dpi=300)
plt.close()


plt.figure(figsize=(12,8))
sns.boxplot(
    x="PC3",
    y="Condition",
    data=coords,
    palette="tab10"
)
plt.xlabel(f"PCoA3 ({var_exp[2]*100:.1f}%)")
plt.title("PCoA3 Boxplot (Bray-Curtis)")
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.tight_layout()
plt.savefig(f"{OUTDIR}/pcoa3_boxplot.png", dpi=300)
plt.close()

#Alpha diversity
alpha_df = compute_alpha(otu)
alpha_df
alpha_df = alpha_df.join(metadata[["Condition", "Location"]])
alpha_df.to_csv(f"{OUTDIR}/alpha_diversity.csv")

##Richness
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

#Shannon
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

#Random Forest
dataMatrix = otu.copy()
dataMatrix["Condition"] = metadata["Condition"]

cols = ["Condition"] + [c for c in dataMatrix.columns if c != "Condition"]
dataMatrix = dataMatrix[cols]

auc_fig, confusion_mat, patient_preds = run_rf_multiclass(
    dataMatrix,
    class_col="Condition",
    auc_outfile=f"{OUTDIR}/rf_auc_curve.png",
    report_txt=f"{OUTDIR}/rf_report.txt"
)

#Differential abundance
metadata_daa = metadata[metadata["Condition"] != "Patient"]
metadata_daa.loc[metadata_daa["Condition"] == "Ulcerative colitis", "Condition"] = "Disease"
metadata_daa.loc[metadata_daa["Condition"] == "Crohn's disease", "Condition"] = "Disease"
group = metadata_daa["Condition"]
otu_daa = otu.loc[metadata_daa.index]
otu_daa = otu_daa + 1e-6

ancom_df, percentile_df = ancom(otu_daa, group)
sig_taxa = ancom_df[ancom_df['Signif']].index
medians= percentile_df[50.0].loc[sig_taxa]
medians['Diff'] = medians['Healthy control'] - medians['Disease']

top_diff = medians['Diff'].abs().sort_values(ascending=False).head(20)
top_taxa = medians.loc[top_diff.index]
top_taxa.to_csv(f"{OUTDIR}/differential_abundance_top_20.csv")

plt.figure(figsize=(8, 6))
plt.bar(top_taxa.index, top_taxa['Diff'])
plt.axhline(0, color='grey', linewidth=0.8, linestyle='--')
plt.ylabel('Median Abundance Difference\n(Disease - Healthy control)')
plt.xlabel('Taxon')
plt.title('Top 20 Significant Taxa: Median Abundance Difference')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(f"{OUTDIR}/differential_abundance.png", dpi=300)
plt.close()

#Visualizing patient species profile
patient = metadata[metadata["Condition"] == "Patient"]
otu_patient = otu.loc[patient.index]

barplot_taxa_facet_fill(
    otu_table=otu_patient,
    taxonomy_series=taxonomy_series,
    metadata=patient,
    level="Species",
    top_n=10,
    fig_width=12,
    height_per_condition=10,
    out_file=f"{OUTDIR}/top10_taxa_patient.png"
)

