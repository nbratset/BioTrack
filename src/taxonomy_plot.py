import pandas as pd
import matplotlib.pyplot as plt

def barplot_taxa(feature_table, taxonomy_series, level="Genus", top_n=10):
    """
    feature_table: samples as rows, OTUs as columns
    taxonomy_series: pandas Series, index = OTUs, value = full taxonomy string
    level: one of "K","P","C","O","F","G","S" or full names like "Genus"
    top_n: number of top taxa to show; rest combined as 'Other'
    """
    # Split taxonomy string into columns
    taxa = taxonomy_series.str.split(";", expand=True)
    taxa.columns = ["K","P","C","O","F","G","S"]

    # Map long level names to short
    level_map = {
        "Kingdom": "K", "Phylum": "P", "Class": "C", "Order": "O",
        "Family": "F", "Genus": "G", "Species": "S"
    }
    col = level_map.get(level, level)  # allow short code directly

    # Group OTUs by taxon and sum abundances
    grouped = feature_table.groupby(taxa[col], axis=1).sum()

    # Convert to relative abundance
    rel = grouped.div(grouped.sum(axis=1), axis=0) * 100

    # Pick top N taxa across all samples
    top_taxa = rel.sum().sort_values(ascending=False).head(top_n).index

    # Build table with top taxa + "Other"
    rel_top = rel[top_taxa].copy()
    rel_top["Other"] = rel.drop(columns=top_taxa, errors="ignore").sum(axis=1)

    # Colors: auto for top taxa, grey for Other
    cmap = plt.get_cmap("tab20")
    num_colors = len(top_taxa)
    colors = [cmap(i) for i in range(num_colors)] + ["grey"]

    # Plot
    rel_top.plot(
        kind="bar",
        stacked=True,
        figsize=(12, 6),
        color=colors
    )

    plt.ylabel("% abundance")
    plt.xlabel("Samples")
    plt.title(f"Relative Abundance at {level} level (Top {top_n} taxa)")
    plt.legend(title=level, bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.show()
