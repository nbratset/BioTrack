import unittest
import sys
from unittest.mock import patch
import pandas as pd
import os
from pathlib import Path
import numpy as np
from skbio import DistanceMatrix

sys.path.append("src")  # noqa

import randomforest
import diversity
import taxonomy_plot

class TestAnalysis(unittest.TestCase):
    """Unit tests for functions used in main.py"""

    def setUp(self):
        """Create small dummy OTU table and metadata for testing"""
        self.otu_table = pd.DataFrame({
            "OTU1": [10, 2, 3],
            "OTU2": [5, 1, 0],
            "OTU3": [10,2,3],
        }, index=["sample1", "sample2", "sample3"])

        self.metadata_table = pd.DataFrame({
            "Condition": ["Disease","Healthy","Disease"],
            "Location": ["USA","Korea","USA"],
        }, index=["sample1", "sample2", "sample3"])

        self.taxonomy_table = pd.Series({
            "OTU1": "K;P;C;O;F;G1;S",
            "OTU2": "K;P;C;O;F;G2;S",
            "OTU3": "K;P;C;O;F;G3;S",
            "OTU4": "K;P;C;O;F;G1;S",
        })

    def test_calc_alpha_div_creates_output_file(self):
        """Ensure compute_alpha works as intended"""
        df = diversity.compute_alpha(self.otu_table)
        self.assertListEqual(list(df.index), ["sample1", "sample2", "sample3"]) #checks whether all samples are retained
        self.assertEqual(df.loc["sample1", "Observed"], 3) #checks whether richness is calulcated correctly- positive test case 
        self.assertNotEqual(df.loc["sample2", "Observed"], 0) #checks whether richness is calulcated correctly- negative test case
        self.assertTrue(df.loc["sample2", "Observed"] > df.loc["sample2", "Shannon"]) #checks for logic because Shannon and Simpson are always less than observed
        self.assertTrue(df.loc["sample2", "Simpson"] < df.loc["sample2", "Observed"]) #checks for logic because Shannon and Simpson are always less than observed
        self.assertTrue(np.isfinite(df["Shannon"]).all()) #checks it's a finite number for all 3 samples
        self.assertTrue(np.isfinite(df["Simpson"]).all()) #checks it's a finite number for all 3 samples
       
        with self.assertRaises(ValueError) as error:
           df2 = diversity.compute_alpha()
        self.assertIn("OTU table not provided.", str(error.exception)) #checks if the error in raised if OTU table is not passed correctly
       

    def test_beta_diversity(self):
        """Ensure calc_beta works as intended"""
        dist = diversity.compute_beta(self.otu_table)
        self.assertIsInstance(dist, DistanceMatrix)
        self.assertListEqual(dist.ids, ["sample1", "sample2", "sample3"]) #checks data structure
        self.assertEqual(dist.shape, (3, 3)) #checks data structure
        for i in range(3):
            self.assertAlmostEqual(dist[i, i], 0.0, places=6) # checks that the distance to itself = 0

        with self.assertRaises(ValueError) as error:
           dist2 = diversity.compute_beta()
        self.assertIn("OTU table not provided.", str(error.exception)) #checks if the error in raised if OTU table is not passed correctly
        
    def test_calc_taxa_top20(self):
        taxonomy_plot.barplot_taxa_facet_fill(self.otu_table, self.taxonomy_table, self.metadata_table, level="Genus", top_n=10, out_file="taxonomy.png")
        self.assertTrue(os.path.exists("taxonomy.png")) #checks that the output is produced
        
        with self.assertRaises(ValueError) as error1:
            taxonomy_plot.barplot_taxa_facet_fill(self.otu_table, self.taxonomy_table, level="Genus", top_n=10, out_file="taxonomy.png")
        self.assertIn("Metadata not provided.", str(error1.exception)) #checks if metadata is not passed properly
        
        taxa_table = pd.Series({
            "OTU1": "K;P;C;O;F;S",
            "OTU2": "K;P;C;O;F;S",
            "OTU3": "K;P;C;O;F;S",
            "OTU4": "K;P;C;O;F;S",})
        with self.assertRaises(ValueError) as error2:
            taxonomy_plot.barplot_taxa_facet_fill(self.otu_table, taxa_table, self.metadata_table, level="Genus", top_n=10, out_file="taxonomy.png")
        self.assertIn("Taxonomy table is missing required taxonomic ranks: Genus", 
                      str(error2.exception)) #checks if the format of the taxonomy_series is valid
 
    def test_random_forest(self):
        dataMatrix = self.otu_table.copy()
        dataMatrix["Condition"] = self.metadata_table["Condition"]
        cols = ["Condition"] + [c for c in dataMatrix.columns if c != "Condition"]
        dataMatrix = dataMatrix[cols]
        
        auc_fig, confusion_mat, patient_preds= randomforest.run_rf_multiclass(dataMatrix, class_col="Condition", auc_outfile="rf.png", report_txt="rf.txt")
        self.assertTrue(os.path.exists("rf.png")) #checks that the output is produced
        self.assertTrue(os.path.exists("rf.txt")) #checks that the output is produced
        self.assertEqual(confusion_mat.shape, (2, 2)) #checks that the output has correct structure
        
        with self.assertRaises(ValueError) as error1:
            randomforest.run_rf_multiclass(dataMatrix, class_col="Disease")
        self.assertIn("Column 'Disease' not found in dataMatrix", str(error1.exception)) #checks whether the error is raised correctly
        
        dataMatrix2 = pd.DataFrame()
        with self.assertRaises(ValueError) as error2:
            randomforest.run_rf_multiclass(dataMatrix2, class_col="Condition")
        self.assertIn("dataMatrix is empty. Check your input table and metadata", str(error2.exception)) #checks whether the error is raised correctly


if __name__ == "__main__":
    unittest.main()
