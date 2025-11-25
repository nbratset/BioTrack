import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def barplot_taxa_facet_fill(
    otu_table, taxonomy_series, metadata, level="Genus", top_n=10, out_file=None
):
    """
    Creates stacked normalized barplots of top N taxa by condition,
    sorting samples by their dominant genus. Only one legend is kept.
    
    Parameters:
        otu_table: DataFrame, samples as rows, OTUs as columns
        taxonomy_series: pandas Series, index=OTUs, value=taxonomy string
        metadata: DataFrame, sample metadata, index=samples, includes 'Condition'
        level: Taxonomy level ("Genus" or short keys "G")
        top_n: Number of top taxa to show (others merged as 'Other')
        out_file: Optional output path for the figure
    """
    # Parse taxonomy
    taxa_df = taxonomy_series.str.split(";", expand=True)
    taxa_df.columns = ["K","P","C","O","F","G","S"]
    lvl_map = {"Kingdom":"K","Phylum":"P","Class":"C","Order":"O","Family":"F","Genus":"G","Species":"S"}
    lvl = lvl_map.get(level, level)
    otu_by_tax = otu_table.T.groupby(taxa_df[lvl]).sum().T

    # Get top taxa, combine others as "Other"
    top_tax = otu_by_tax.sum().sort_values(ascending=False).head(top_n).index.tolist()
    otu_top = otu_by_tax[top_tax].copy()
    otu_top["Other"] = otu_by_tax.drop(columns=top_tax, errors="ignore").sum(axis=1)

    # Normalize abundances per sample
    otu_top_rel = otu_top.div(otu_top.sum(axis=1), axis=0)

    # Merge with metadata
    otu_top_rel["Sample"] = otu_top_rel.index
    otu_top_rel["Condition"] = metadata.loc[otu_top_rel.index, "Condition"]
    df_melt = otu_top_rel.melt(id_vars=["Sample","Condition"], var_name="Taxa", value_name="Proportion")

    # Pivot for easier plotting
    taxa_order = top_tax + ["Other"]
    pivot_df = df_melt.pivot_table(index=["Sample", "Condition"], columns="Taxa", values="Proportion").fillna(0)

    # Colors: ensure enough for all taxa, use 'tab20' (colorblind-safe alternative: 'colorblind')
    color_palette = sns.color_palette("tab20", n_colors=len(taxa_order))
    genus_sums = pivot_df[taxa_order].sum(axis=0)
    most_abundant_genus = genus_sums.idxmax()

        # Prepare figure
    conditions = pivot_df.index.get_level_values('Condition').unique()
    nconds = len(conditions)
    fig, axes = plt.subplots(nconds, 1, figsize=(22, 4*nconds), sharey=True)
    axes = [axes] if nconds == 1 else axes

    # Plot loop; sort by globally most abundant genus
    for i, (ax, condition) in enumerate(zip(axes, conditions)):
        cond_df = pivot_df.xs(condition, level="Condition")
        sorted_samples = cond_df[most_abundant_genus].sort_values(ascending=False).index
        cond_df_sorted = cond_df.loc[sorted_samples]

        bottom = None
        for idx, taxa in enumerate(taxa_order):
            values = cond_df_sorted[taxa] if taxa in cond_df_sorted else 0
            ax.bar(cond_df_sorted.index, values, bottom=bottom, label=taxa, color=color_palette[idx], width=1)
            bottom = values if bottom is None else bottom + values

        ax.set_title(f"Condition = {condition}", fontsize=15)
        ax.set_ylabel("Proportion")
        ax.set_xlabel("Sample")
        ax.set_xticklabels([])  # disables x-axis tick labels
        ax.grid(axis='x', linestyle='', linewidth=0)
        if i == nconds - 1:
            ax.legend(loc='upper right', bbox_to_anchor=(1.1,1), fontsize=12)

    fig.suptitle(f"Top {top_n} {level}-Level Taxa by Condition", fontsize=18)
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)

    if out_file:
        plt.savefig(out_file, dpi=300, bbox_inches="tight")
        plt.close()
    else:
        plt.show()
