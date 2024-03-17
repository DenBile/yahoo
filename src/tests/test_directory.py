from enum import Enum
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from modules.directory import create_direcotry, DirNotCreateException

class TestPath(Enum):
    EXISTING_PATH = '/existing/directory'
    NEW_PATH = '/new/directory'

class TestCreateDirectory(unittest.TestCase):
    @patch('pathlib.Path.resolve')
    def test_create_directory_exists(self, mock_resolve):
        mock_resolve.return_value.exists.return_value = True
        create_direcotry(Path(TestPath.EXISTING_PATH.value))
        mock_resolve.assert_called_once()
        mock_resolve.return_value.mkdir.assert_not_called()  # Corrected assertion

    @patch('pathlib.Path.resolve')
    @patch('pathlib.Path.mkdir')
    def test_create_directory_failure(self, mock_mkdir, mock_resolve):
        mock_resolve.return_value.exists.return_value = False
        mock_mkdir.side_effect = Exception('Test exception')
        with self.assertRaises(Exception):
            create_direcotry(Path(TestPath.NEW_PATH.value))
        mock_resolve.assert_called_once()
        mock_mkdir.assert_called_once_with(parents=True)

    @patch('pathlib.Path.resolve')
    @patch('pathlib.Path.mkdir')
    def test_create_directory_not_created_exception(self, mock_mkdir, mock_resolve):
        mock_resolve.return_value.exists.return_value = False
        mock_mkdir.return_value.exists.return_value = False
        with self.assertRaises(DirNotCreateException):
            create_direcotry(Path(TestPath.NEW_PATH.value))
        mock_resolve.assert_called_once()
        mock_mkdir.assert_called_once_with(parents=True)

if __name__ == '__main__':
    unittest.main()