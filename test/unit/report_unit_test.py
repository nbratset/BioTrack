import sys
import unittest
import pandas as pd

sys.path.append('src/')  # noqa
sys.path.append('test/unit/')  # noqa

import app


class TestReport(unittest.TestCase):
    def test_parse_csvs(self):
        taxa_file = 'input_data/otu.csv'
        alpha_file = 'results/alpha_diversity.csv'
        beta_file = 'results/beta_diversity_coords.csv'
        diff_file = 'results/differential_abundance_top_20.csv'
        df1, df2, df3, df4 = app.parse_csvs(taxa_file,
                                            alpha_file,
                                            beta_file,
                                            diff_file)
        # I'll test for sys.exit(0) here if you have a bad file.
        self.assertEqual(app.get_patient('bad.csv',
                                         alpha_file,
                                         beta_file,
                                         diff_file),
                                        'Missing Taxa/OTU File')
        self.assertEqual(app.get_patient(taxa_file,
                                         'bad.csv',
                                         beta_file,
                                         diff_file),
                                        'Missing alpha diversity File')
        self.assertEqual(app.get_patient(taxa_file,
                                         alpha_file,
                                         'bad.csv',
                                         diff_file),
                                        'Missing beta diversity File')
        self.assertEqual(app.get_patient(taxa_file,
                                         alpha_file,
                                         beta_file,
                                         'bad.csv'),
                                        'Missing Differential Abundance File')  # noqa

    def test_get_patient(self):
        alpha_file = 'results/alpha_diversity.csv'
        df = pd.read_csv(alpha_file)
        self.assertEqual(app.get_patient(df), 'SRR5946632')

    def test_parse_rf(self):
        self.assertEqual(app.parse_rf_export('rf_report.txt'),
                         'Healthy Control')

    def test_parse_rf_errors(self):
        self.assertEqual(app.parse_rf_export('bad.txt'),
                         'Cannot find RF_report File!')
