import logging
from pathlib import Path

from .directory import create_direcotry

from models.log_levels import LogLevel


class Logger:
    
    def __init__(
            self,
            app_name: str,
            level: LogLevel,
            format: str = f'{"%(asctime)s":>10} | {"%(levelname)s":>10} | %(message)s',
            date_format: str = '%d-%m-%Y %H:%M:%S',
            enable_console_logging: bool = True
        ) -> None:

        self._log_dir = Path('../logs')
        self._log_file = f'process_{app_name}.log'

        self._set_logging_directory()
        handlers = self._set_handlers(enable_console_logging=enable_console_logging)

        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(level)

        formatter = logging.Formatter(format, date_format)

        for handler in handlers:
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

    def _set_logging_directory(self) -> None:
        '''
        Creates the logging direcotry if it does not exist, otherwise creates it.
        '''
        
        create_direcotry(self._log_dir)

    def _set_handlers(self, enable_console_logging: bool) -> list[logging.FileHandler]:
        '''
        Create logging file if it does not exist.
        If the file exist it will rename it to the current date-time and create a new one for the current execution.
        '''

        handlers = [logging.FileHandler(filename=self._log_dir/self._log_file, mode='a')]
        
        if enable_console_logging:
            handlers.append(logging.StreamHandler())
        
        return handlers

    def debug(self, message: str) -> None:
        '''
        A method to log debug level messages.
        '''

        self._logger.debug(message)

    def info(self, message: str) -> None:
        '''
        A method to log info level messages.
        '''
        
        self._logger.info(message)

    def warning(self, message: str) -> None:
        '''
        A method to log warning level messages.
        '''
        
        self._logger.warning(message)

    def error(self, message: str) -> None:
        '''
        A method to log error level messages.
        '''
        
        self._logger.error(message)

    def critical(self, message: str) -> None:
        '''
        A method to log critical level messages.
        '''
        
        self._logger.critical(message)