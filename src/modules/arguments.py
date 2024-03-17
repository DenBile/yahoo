import re
import argparse

from models.report import ReportRanges
from models.log_levels import LogLevel

def ticker_regex_type(user_passed_argument: str, pattern=re.compile(r'^[a-zA-Z0-9!@#$&()\\-`.+,/\"]{2,}$')):
    if not pattern.match(user_passed_argument):
        raise argparse.ArgumentTypeError('Invalid value for ticker.')
    return user_passed_argument

def get_arguments(scrapper: bool):
    '''
    A helper function that will be used to parse arguments to the script.
    '''
    
    parser = argparse.ArgumentParser(description='Details for a Yahoo finance tracker.')

    parser.add_argument(
        '-t',
        '--ticker',
        type=ticker_regex_type,
        default='0P00000QX4.L',
        help='A ticker that you would like to track.'
    )
    parser.add_argument(
        '-ll',
        '--log_level',
        type=str,
        choices=[available_level.value for available_level in LogLevel],
        default=LogLevel.INFO.value,
        required=False,
        help='<Optional> Log level if a logfile. Default value is INFO.'
    )

    if scrapper:
        parser.add_argument(
            '-rr',
            '--report_range',
            type=str,
            choices=[available_range.value for available_range in ReportRanges],
            default=ReportRanges.YEAR.value,
            help='A ticker that you would like to track.'
        )
        return parser.parse_args()
    
    parser.add_argument(
        '-s',
        '--server',
        type=str,
        default='127.0.0.1',
        required=False,
        help='<Optional> Server host address where the package will be sent with the details for a ticker. Default value is 127.0.0.1'
    )
    parser.add_argument(
        '-p',
        '--port',
        type=int,
        default=30000,
        required=False,
        help='<Optional> Server port where the package will be sent with the details for a ticker. Default value is 30000'
    )

    return parser.parse_args()
