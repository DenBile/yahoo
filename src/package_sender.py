import json
from pathlib import Path

from models.argument import ClientArgument

from modules.file import get_file_name
from modules.arguments import get_arguments

from modules.logger import Logger
from modules.reports import Report
from modules.socket.client import TCPClient


def main():
    '''
    Main function for executing the client script.
    '''

    args = get_arguments(scrapper=False)
    arguments = ClientArgument(
        ticker=args.ticker,
        log_level=args.log_level,
        server=args.server,
        port=args.port
    )

    log = Logger(app_name=get_file_name(path=__file__), level=arguments.log_level)
    log.info('Execution started')
    log.debug(f'Arguments parsed {arguments}')
    
    report = Report(log=log, dir=Path('../reports').resolve(), ticker=arguments.ticker)

    if not report.file_exists:
        log.error('Unable to open file, as it does not exists')
        log.info('Execution complete')
        return
    
    df_yahoo_historical_details = report.open_existing_excel_file()

    log.debug('Converting DataFrame to dict')
    yahoo_historical_data = df_yahoo_historical_details.to_dict()
    
    with TCPClient(log=log, host=arguments.server, port=arguments.port) as client_socket:
        client_socket.send_all(data=json.dumps(yahoo_historical_data['Close']))
        client_socket.disconnect()

    log.info('Execution complete')

if __name__ == '__main__':
    main()