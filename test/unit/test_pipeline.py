import sys
import unittest

sys.path.append('src/')  # noqa
sys.path.append('test/unit/')  # noqa

import app


class TestReport(unittest.TestCase):
    def test_app(self):
        # my goal here is to use test-first dev to build in error handling
        self.assertEqual()
        '''
        Just kinda brainstorming here, I think I want to make sure that I:
         - properly read in the processed data files,
         - process them correctly for plotting
         - run the app
        '''
        # Test file import/reading
        # Test file processing for plotting (pandas type stuff)
        # Test that the full app program runs w/o error
