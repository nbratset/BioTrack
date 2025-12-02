import pandas as pd
from skbio.diversity import beta_diversity
import numpy as np


def compute_alpha(otu_table):
    """
    Compute alpha diversity:
      - Observed richness (# OTUs with non-zero counts)
      - Shannon
      - Simpson

    otu_table: DataFrame
        rows = samples
        columns = OTUs
        values = counts or relative abundances
    """

    # Error handling###
    if otu_table is None:
        raise ValueError("OTU table not provided.")

    if otu_table.isna().any().any():
        raise ValueError("OTU table contains missing values.")

    if not np.issubdtype(otu_table.dtypes.values[0], np.number):
        raise ValueError("OTU table must contain numeric values only.")

    #####

    # ---- Alpha metric functions ----
    def shannon(counts):
        total = counts.sum()
        if total == 0:
            return 0
        p = counts / total
        p = p[p > 0]
        return -(p * np.log(p)).sum()

    def simpson(counts):
        total = counts.sum()
        if total == 0:
            return 0
        p = counts / total
        return 1 - (p**2).sum()

    # ---- Compute metrics ----
    results = pd.DataFrame(index=otu_table.index)

    # Observed richness = number of OTUs with abundance > 0 for each sample
    results["Observed"] = (otu_table > 0).sum(axis=1)

    # Shannon & Simpson
    results["Shannon"] = otu_table.apply(shannon, axis=1)
    results["Simpson"] = otu_table.apply(simpson, axis=1)

    return results


def compute_beta(otu_table):
    """
    Compute Bray-Curtis beta diversity distance matrix
    feature_table: pandas DataFrame, samples as rows, OTUs as columns
    Returns: skbio DistanceMatrix
    """

    # Error handling###
    if otu_table is None:
        raise ValueError("OTU table not provided.")

    if otu_table.isna().any().any():
        raise ValueError("OTU table contains missing values.")

    if not np.issubdtype(otu_table.dtypes.values[0], np.number):
        raise ValueError("OTU table must contain numeric values only.")

    #####

    beta = beta_diversity(
        metric="braycurtis",
        counts=otu_table.values,  # samples are rows
        ids=otu_table.index
    )
    return beta
