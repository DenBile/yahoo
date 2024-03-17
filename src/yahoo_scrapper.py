import yfinance
import pandas as pd
from pathlib import Path

from models.argument import ScrapperArgument

from modules.file import get_file_name
from modules.arguments import get_arguments

from modules.logger import Logger
from modules.reports import Report


def main():
    '''
    Main function for downloading data from Yahoo finance via API script.
    '''

    args = get_arguments(scrapper=True)
    arguments = ScrapperArgument(
        ticker=args.ticker,
        report_range=args.report_range,
        log_level=args.log_level
    )

    log = Logger(app_name=get_file_name(path=__file__), level=arguments.log_level)
    
    log.info('Execution started')
    log.debug(f'Arguments parsed {arguments}')

    report = Report(log=log, dir=Path('../reports').resolve(), ticker=arguments.ticker)
    log.debug(f'Report directory created {report.dir.as_posix()}')

    try:
        log.info('Fetching data from Yahoo finance')
        yahoo_details = yfinance.Ticker(arguments.ticker)
    except Exception as exception_message:
        log.critical('Unexpected exception occured while fetching data from Yahoo finance.')
        log.error(exception_message)
        raise Exception
    else:
        log.debug(f'Report for the past {arguments.report_range}')
        df_yahoo_details = yahoo_details.history(period=arguments.report_range)

        log.info('Removing timezone from a DataFrame and converting it to string')
        df_yahoo_details.index = df_yahoo_details.index.tz_localize(None).strftime('%Y-%m-%d')
        log.debug(f'\n{df_yahoo_details}')
    
    # Keep only Date (index) and Close columns.
    # Access them by index since the other columns may change over time.
    log.info('Dropping all columns except "Date" and "Close"')
    df_yahoo_details = df_yahoo_details[['Close']]

    if not report.file_exists:
        report.create_new_excel_file(data=df_yahoo_details)
        log.info('Execution complete')
        return
    
    df_yahoo_historical_details = report.open_existing_excel_file()

    # If historical data file existed, but was empty, just add new data there.
    if df_yahoo_historical_details.empty:
        report.extend_excel_file(data=df_yahoo_details)
        log.info('Historical data file was empty, added new items')
        log.info('Execution complete')
        return
    
    latest_eod = df_yahoo_historical_details.iloc[-1].name

    # Exit if the historical file contains the latest data already
    if latest_eod == df_yahoo_details.iloc[-1].name:
        log.warning('Historical data already contains the latest updates')
        log.info('Execution complete')
        return 

    latest_row_date_in_hist_file = df_yahoo_historical_details[df_yahoo_historical_details.index == latest_eod]
    latest_date = latest_row_date_in_hist_file.iloc[0].name

    # Exit if the historical data is too old since the current run doesn't have any of the dates from that file 
    if latest_date not in df_yahoo_details.index.unique():
        log.warning(f'The latest date in a file is {latest_date}, however, it\'s not present in current report. Therefore the sciprt can\'t extend the table. Please increase the range of search and try again.')
        log.info('Execution complete')
        return
    
    df_new_records = df_yahoo_details[df_yahoo_details.index > latest_date]
    log.debug(f'New ({len(df_new_records)}) records will be added to the existing Excel file\n{df_new_records}')
    
    df_extended_data = pd.concat([df_yahoo_historical_details, df_new_records])
    report.extend_excel_file(data=df_extended_data)
    log.info('Historical data extended')
    log.info('Execution complete')
     
if __name__ == '__main__':
    main()