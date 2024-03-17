import unittest
from unittest.mock import Mock, patch
from pathlib import Path
import pandas as pd

from modules.reports import Report

class TestReport(unittest.TestCase):

    def setUp(self):
        self.log = Mock()
        self.dir = Path('./test_reports')
        self.ticker = 'TEST'
        self.report = Report(log=self.log, dir=self.dir, ticker=self.ticker)

    def test_file_exists(self):
        with patch('pathlib.Path.is_file') as mock_is_file:
            # Test case where file exists
            mock_is_file.return_value = True
            self.assertTrue(self.report.file_exists)

            # Test case where file does not exist
            mock_is_file.return_value = False
            self.assertFalse(self.report.file_exists)

if __name__ == '__main__':
    unittest.main()