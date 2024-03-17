import unittest
from unittest.mock import Mock, patch
from modules.socket.server import TCPServer

class TestTCPServer(unittest.TestCase):

    def setUp(self):
        self.log = Mock()
        self.host = '127.0.0.1'
        self.port = 3000
        self.max_connections = 5
        self.server = TCPServer(log=self.log, host=self.host, port=self.port, max_connections=self.max_connections)

    @patch('socket.socket')
    def test_connect_success(self, mock_socket):
        mock_connection = mock_socket.return_value
        self.server._connect()
        mock_connection.bind.assert_called_once_with((self.host, self.port))
        mock_connection.listen.assert_called_once_with(self.max_connections)
        self.assertTrue(self.server._is_connected)

    @patch('socket.socket')
    def test_connect_failure(self, mock_socket):
        mock_socket.side_effect = Exception('Connection error')
        with self.assertRaises(Exception):
            self.server._connect()
        self.assertFalse(self.server._is_connected)

    @patch('socket.socket')
    def test_disconnect(self, mock_socket):
        mock_connection = mock_socket.return_value
        self.server._socket_connection = mock_connection
        self.server._disconnect()
        mock_connection.close.assert_called_once()
        self.assertIsNone(self.server._socket_connection)

if __name__ == '__main__':
    unittest.main()