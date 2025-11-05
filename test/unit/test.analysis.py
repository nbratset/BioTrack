import unittest
import sys
from unittest.mock import patch
import pandas as pd
import os
from pathlib import Path

sys.path.append("src")  # noqa

import analysis #store analysis as a python file first (currently it is a notebook)

class TestAnalysis(unittest.TestCase):
    """Unit tests for functions in analysis.py"""

    def setUp(self):
        """Create small dummy OTU table and metadata for testing."""
        self.otu_table = pd.DataFrame({
            "OTU1": [10, 0, 3],
            "OTU2": [5, 1, 0],
            "OTU3": [0, 7, 2],
        }, index=["sample1", "sample2", "sample3"])

        self.metadata = pd.DataFrame({
            "Lifestyle": ["Urban", "Rural", "Urban"],
            "Age.C": [25, 40, 35],
            "Altitude": [100, 200, 150],
            "Latitude": [30.1, 31.5, 29.7],
            "Sex": ["M", "F", "M"]
        }, index=["sample1", "sample2", "sample3"])

    def test_calc_alpha_div_creates_output_file(self):
        """Ensure calc_alpha_div creates the expected output file."""
        analysis.calc_alpha_div(self.otu_table, self.metadata)
        self.assertTrue(os.path.exists("alpha_diversity_metrics.tsv"))

    @patch("analysis.ro.r")
    
    
    def test_maaslin_file_creation_and_r_call(self, mock_r):
        """Verify MaAsLin2 input files are written, R is called, and outputs are correct."""
        outdir = Path("maaslin2_output")

        # Run function
        r_out, df_meta = analysis.maaslin(self.otu_table, self.metadata)

        # 1️⃣ Check that input files were created
        data_file = outdir / "maaslin_input.tsv"
        meta_file = outdir / "maaslin_meta.tsv"
        self.assertTrue(data_file.exists())
        self.assertTrue(meta_file.exists())

        # 2️⃣ Check metadata is returned unchanged
        pd.testing.assert_frame_equal(df_meta, self.metadata)

        # 3️⃣ Verify R command was invoked
        mock_r.assert_called_once()
        self.assertIn("Maaslin2", mock_r.call_args[0][0])

        # 4️⃣ Verify output directory path returned
        self.assertIn("maaslin2_output", r_out)
    
    
    def test_calc_taxa_top20_and_grouping(self):
        result = analysis.calc_taxa(self.otu_table, self.metadata)

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


if __name__ == "__main__":
    unittest.main()
