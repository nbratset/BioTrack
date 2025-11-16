from skbio.stats.ordination import pcoa

def run_pcoa(distance_matrix):
    """
    distance_matrix: square matrix (samples x samples), pandas DataFrame or skbio.DistanceMatrix
    Returns:
        pcoa_results: DataFrame with sample coordinates along PCoA axes
        explained_variance: Series of variance explained by each axis
    """
    ord_res = pcoa(distance_matrix)
    pcoa_results = ord_res.samples
    explained_variance = ord_res.proportion_explained
    return pcoa_results, explained_variance
