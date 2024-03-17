import argparse
import unittest
from unittest.mock import patch
from argparse import ArgumentTypeError
from modules.arguments import get_arguments, ticker_regex_type

DEFAULT_TICKER = '0P00000QX4.L'
DEFAULT_LOG_LEVEL = 'INFO'
DEFAULT_REPORT_RANGE = 'YEAR'
TEST_TICKER = 'JPM'
TEST_INVALID_TICKER = '@DENYS%BILETSKYY'

class TestGetArguments(unittest.TestCase):
    @patch('argparse.ArgumentParser.parse_args')
    def test_get_arguments_default(self, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(
            ticker=DEFAULT_TICKER,
            log_level=DEFAULT_LOG_LEVEL
        )
        args = get_arguments(scrapper=False)
        self.assertEqual(args.ticker, DEFAULT_TICKER)
        self.assertEqual(args.log_level, DEFAULT_LOG_LEVEL)

    @patch('argparse.ArgumentParser.parse_args')
    def test_get_arguments_scrapper(self, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(
            ticker=DEFAULT_TICKER,
            log_level=DEFAULT_LOG_LEVEL,
            report_range=DEFAULT_REPORT_RANGE
        )
        args = get_arguments(scrapper=True)
        self.assertEqual(args.ticker, DEFAULT_TICKER)
        self.assertEqual(args.log_level, DEFAULT_LOG_LEVEL)
        self.assertEqual(args.report_range, DEFAULT_REPORT_RANGE)

    def test_ticker_regex_type_valid(self):
        self.assertEqual(ticker_regex_type(TEST_TICKER), TEST_TICKER)

    def test_ticker_regex_type_invalid(self):
        with self.assertRaises(ArgumentTypeError):
            ticker_regex_type(TEST_INVALID_TICKER)

if __name__ == '__main__':
    unittest.main()