import sys
import unittest

sys.path.append('src/')  # noqa
sys.path.append('test/unit/')  # noqa

import run_pipeline


class TestReport(unittest.TestCase):
    def test_args(self):
        # my goal here is to use test-first dev to build in error handling
        self.assertEqual()
 