import sys
import unittest

sys.path.append('src/')  # noqa
sys.path.append('test/unit/')  # noqa

import app


class TestReport(unittest.TestCase):
    def test_import(self):
        # I want this function to import 3 csvs and export them as dataframes
        # I want it to export as 3 different dataframes
        # taxa_file, alpha_file, beta_file will come from commandline
        # import input_data/otu.csv
        # import results/alpha_diversity.csv
        # import results/beta_diversity_coords.csv
        taxa_file = 'input_data/otu.csv'
        alpha_file = 'results/alpha_diversity.csv'
        beta_file = 'results/beta_diversity_coords.csv'
        df1, df2, df3 = app.parse_csvs(taxa_file, alpha_file, beta_file)
        self.assertEqual()  # ??
    
    def test_import_errors(self):
        taxa_file = 'input_data/otu.csv'
        alpha_file = 'results/alpha_diversity.csv'
        beta_file = 'results/beta_diversity_coords.csv'
        df1, df2, df3 = app.parse_csvs(taxa_file, alpha_file, beta_file)
        # I'll test for sys.exit(0) here if you have a bad file. 

    def test_parse_rf(self):
        # I want this to parse the rf file for the patient prediction
        self.assertEqual(app.parse_rf_export('rf_report.txt'), 'Healthy Control')
    
    def test_parse_rf_errors(self):
        # test if the file exists/is empty
        # I want sys.exit(0) for controlled errors
        pass