import sys
sys.path.append("src")

import pandas as pd
from diversity import compute_alpha, compute_beta
from ordination import run_pcoa
from taxonomy_plot import barplot_taxa
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
otu = pd.read_csv("input_data/otu.csv", index_col=0)      # samples as rows, OTUs as columns
tax = pd.read_csv("input_data/tax.csv", index_col=0)      # ASV/OTU as index, taxonomy strings as values
metadata = pd.read_csv("input_data/metadata.csv", index_col=0)

# Visualization of top 10 species
taxonomy_series = tax.apply(lambda row: ";".join(row.values.astype(str)), axis=1)
taxonomy_series.index = tax.index
barplot_taxa(otu, taxonomy_series, level="Genus", top_n=10)

# Beta diversity analysiss
beta = compute_beta(otu)
coords, var_exp = run_pcoa(beta)
coords = coords.join(metadata["Condition"])

plt.figure(figsize=(8,6))
sns.scatterplot(
    x="PC1",
    y="PC2",
    data=coords,
    s=100,   
    hue="Condition",            
    color="cornflowerblue",  
    edgecolor="k"
)
plt.xlabel(f"PCoA1 ({var_exp[0]*100:.1f}%)" if 'var_exp' in locals() else "PC1")
plt.ylabel(f"PCoA2 ({var_exp[1]*100:.1f}%)" if 'var_exp' in locals() else "PC2")
plt.title("PCoA Plot (Bray-Curtis)")
plt.show()

#Alpha diversity
alpha_df = compute_alpha(otu)
alpha_df
alpha_df = alpha_df.join(metadata["Condition"])

plt.figure(figsize=(8,6))

sns.boxplot(
    x="Condition",
    y="Observed",
    data=alpha_df,
    showcaps=True,
    boxprops={'alpha': 0.7},
)

sns.stripplot(
    x="Condition",
    y="Observed",
    data=alpha_df,
    color="black",
    size=6,
    jitter=True,
    alpha=0.8
)

plt.xlabel("Condition")
plt.ylabel("Observed richness")
plt.title("Alpha Diversity (Observed Richness)")
plt.tight_layout()
plt.show()






