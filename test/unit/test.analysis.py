import unittest
import sys

sys.path.append("src")  # noqa

import analysis #store analysis as a python file first (currently it is a notebook)

class TestFileLib(unittest.TestCase):
    def test_calc_alpha_diversity(self):
        # Create dummy OTU table
        otu_table = pd.DataFrame({
            "OTU1": [10, 0, 3],
            "OTU2": [5, 1, 0],
            "OTU3": [0, 7, 2],
        }, index=["sample1", "sample2", "sample3"])

        # Create dummy metadata
        metadata = pd.DataFrame({
            "Lifestyle": ["Urban", "Rural", "Urban"],
            "Age.C": [25, 40, 35],
            "Altitude": [100, 200, 150],
            "Latitude": [30.1, 31.5, 29.7],
            "Sex": ["M", "F", "M"]
        }, index=["sample1", "sample2", "sample3"])

        # Run function (creates file)
        analysis.calc_alpha_div(otu_table, metadata)

        # Check file existence
        self.assertTrue(os.path.exists("alpha_diversity_metrics.tsv"))

class TestCalcTaxa(unittest.TestCase):
    def test_calc_taxa_top20_and_grouping(self):
        # Create dummy OTU table (3 taxa × 4 samples)
        otu_table = pd.DataFrame({
            "sample1": [10, 0, 3],
            "sample2": [5, 1, 0],
            "sample3": [0, 7, 2],
            "sample4": [8, 0, 0],
        }, index=["TaxonA", "TaxonB", "TaxonC"])

        # Create dummy metadata
        metadata = pd.DataFrame({
            "Lifestyle": ["Urban", "Rural", "Urban", "Rural"],
        }, index=["sample1", "sample2", "sample3", "sample4"])

        # Run function
        result = analysis.calc_taxa(otu_table, metadata)

        # Basic structure checks
        self.assertIn("Taxon", result.columns)
        self.assertIn("Lifestyle", result.columns)
        self.assertIn("Abundance", result.columns)

        # Grouping check: must have one row per (Lifestyle, Taxon)
        grouped = result.groupby(["Lifestyle", "Taxon"]).size().reset_index()
        self.assertTrue(all(grouped[0] == 1))

        # Content check: values are numeric and nonnegative
        self.assertTrue((result["Abundance"] >= 0).all())

        # Top 20 behavior: since only 3 taxa, should return 3 unique ones
        self.assertEqual(result["Taxon"].nunique(), 3)

