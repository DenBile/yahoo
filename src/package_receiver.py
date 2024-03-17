from modules.file import get_file_name
from modules.arguments import get_arguments

from modules.logger import Logger
from models.argument import ClientArgument
from modules.socket.server import TCPServer


def main():
    '''
    Main function for executing the server script.
    '''

    args = get_arguments(scrapper=False)
    arguments = ClientArgument(
        ticker=args.ticker,
        log_level=args.log_level,
        server=args.server,
        port=args.port
    )
    
    log = Logger(app_name=get_file_name(__file__), level=arguments.log_level)
    log.info('Execution started')
    log.debug(f'Arguments parsed {arguments}')

    with TCPServer(log=log, host=arguments.server, port=arguments.port) as server_socket:
        server_socket.accept_messages()
    
    log.info('All connections closed')
    log.info('Execution complete')

if __name__ == '__main__':
    main()