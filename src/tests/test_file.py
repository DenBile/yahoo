from enum import Enum
import unittest
from unittest.mock import patch
from modules.file import get_file_name

EXPECTED_RESULT = 'test_file_name'

class OS(Enum):
    WINDOWS = 'Windows'
    LINUX = 'Linux'

class Paths(Enum):
    WINDOWS_WITH_EXTENSION = f'C:\\path\\to\\file\\{EXPECTED_RESULT}.txt'
    WINDOWS_WITHOUT_EXTENSION = f'C:\\path\\to\\file\\{EXPECTED_RESULT}'
    LINUX_WITH_EXTENSION = f'/path/to/file/{EXPECTED_RESULT}.txt'
    LINUX_WITHOUT_EXTENSION = f'/path/to/file/{EXPECTED_RESULT}.txt'


class TestGetFileName(unittest.TestCase):
    @patch('platform.system')
    def test_get_file_name_with_extension_windows(self, mock_system):
        mock_system.return_value = OS.WINDOWS.value
        self.assertEqual(get_file_name(Paths.WINDOWS_WITH_EXTENSION.value), EXPECTED_RESULT)

    @patch('platform.system')
    def test_get_file_name_without_extension_windows(self, mock_system):
        mock_system.return_value = OS.WINDOWS.value
        self.assertEqual(get_file_name(Paths.WINDOWS_WITHOUT_EXTENSION.value), EXPECTED_RESULT)

    @patch('platform.system')
    def test_get_file_name_with_extension_linux(self, mock_system):
        mock_system.return_value = OS.LINUX.value
        self.assertEqual(get_file_name(Paths.LINUX_WITH_EXTENSION.value), EXPECTED_RESULT)

    @patch('platform.system')
    def test_get_file_name_without_extension_linux(self, mock_system):
        mock_system.return_value = OS.LINUX.value
        self.assertEqual(get_file_name(Paths.LINUX_WITHOUT_EXTENSION.value), EXPECTED_RESULT)

if __name__ == '__main__':
    unittest.main()