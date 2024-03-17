import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock, call
from modules.logger import Logger, LogLevel


class TestLogger(unittest.TestCase):

    def test_logger_with_console_logging(self):
        # Mock create_direcotry
        with patch('modules.directory.create_direcotry'):
            # Initialize logger with console logging enabled
            logger = Logger(app_name='test_app', level='DEBUG', enable_console_logging=True)
            
            # Assertions
            self.assertEqual(len(logger._logger.handlers), 2)

    def test_log_messages(self):
        # Mock logger
        mock_logger = MagicMock()
        logger_instance = MagicMock()
        mock_logger.return_value = logger_instance

        with patch('logging.getLogger', mock_logger):
            # Initialize logger
            logger = Logger(app_name='test_app', level='DEBUG')
            
            # Log messages at different levels
            logger.debug('Debug message')
            logger.info('Info message')
            logger.warning('Warning message')
            logger.error('Error message')
            logger.critical('Critical message')

            # Assertions
            expected_calls = [
                call.debug('Debug message'),
                call.info('Info message'),
                call.warning('Warning message'),
                call.error('Error message'),
                call.critical('Critical message')
            ]
            logger_instance.assert_has_calls(expected_calls)

if __name__ == '__main__':
    unittest.main()