import pickle
import unittest
from unittest.mock import Mock, patch
from modules.socket.client import TCPClient

class TestTCPClient(unittest.TestCase):

    def setUp(self):
        self.log = Mock()
        self.host = '127.0.0.1'
        self.port = 3000
        self.client = TCPClient(log=self.log, host=self.host, port=self.port)

    @patch('socket.socket')
    def test_connect_success(self, mock_socket):
        mock_connection = mock_socket.return_value
        self.client._connect()
        mock_connection.connect.assert_called_once_with((self.host, self.port))
        self.assertTrue(self.client._is_connected)

    @patch('socket.socket')
    def test_connect_failure(self, mock_socket):
        mock_socket.side_effect = Exception('Connection error')
        with self.assertRaises(Exception):
            self.client._connect()
        self.assertFalse(self.client._is_connected)

    @patch('socket.socket')
    def test_send_all_success(self, mock_socket):
        mock_connection = mock_socket.return_value
        mock_recv = Mock(return_value=pickle.dumps('!SUCCESS'))
        mock_connection.recv = mock_recv
        data = {'key': {'nested_key': 1.0}}
        self.client._socket_connection = mock_connection
        self.client.send_all(data)
        mock_connection.sendall.assert_called()
        mock_recv.assert_called_once()
        self.log.info.assert_called_with('All data sent successfully')

    @patch('socket.socket')
    def test_send_all_failure(self, mock_socket):
        mock_connection = mock_socket.return_value
        mock_recv = Mock(return_value=pickle.dumps('!ERROR'))
        mock_connection.recv = mock_recv
        data = {'key': {'nested_key': 1.0}}
        self.client._socket_connection = mock_connection
        with self.assertRaises(Exception):
            self.client.send_all(data)
        mock_connection.sendall.assert_called()
        mock_recv.assert_called_once()
        self.log.critical.assert_called_with('Server did respond with !SUCCESS after receiving the message!')

    @patch('socket.socket')
    def test_disconnect(self, mock_socket):
        mock_connection = mock_socket.return_value
        self.client._socket_connection = mock_connection
        self.client.disconnect()
        mock_connection.sendall.assert_called_with(b'!DISCONNECT')
        self.log.info.assert_called_with('Disconnect message sent successfully')

if __name__ == '__main__':
    unittest.main()