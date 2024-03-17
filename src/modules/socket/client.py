import pickle
import socket

from modules.chunker import chunker

from modules.logger import Logger
from modules.socket.tcp import TCPSocket


class TCPClient(TCPSocket):
    '''
    Class for managing TCP socket connections.
    '''


    def __init__(self, log: Logger, host: str, port: int) -> None:
        '''
        Initializes the TCPSocket object.

        Args:
            host (str): The host address to connect to.
            port (int): The port number to connect to.
        '''

        self.log = log
        self.host = host

        try:
            self.port = int(port)
        except Exception as exception_message:
            self.log.critical('Unable to convert port into a number')
            self.log.error(exception_message)

        self._socket_connection = None

    def _connect(self) -> None:
        '''
        Establishes a connection with the server.
        '''

        try:
            self.log.info(f'Establishing connection >>> host: {self.host} port: {self.port}')
            self._socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket_connection.connect((self.host, self.port))
        except socket.error as error:
            self.log.critical('Exception occured while establishing a connection')
            self.log.error(error)

            if self._socket_connection:
                self._socket_connection.close()
            raise Exception
        except Exception as exception_message:
            self.log.critical('Unexpected exception occured while establishing a connection')
            self.log.error(exception_message)

            if self._socket_connection:
                self._socket_connection.close()
            raise Exception
        else:
            self.log.info('Connection established successfully')
        
    def _disconnect(self) -> None:
        '''
        Closes the connection with the server.
        '''

        if not self._socket_connection:
            return
        
        self.log.info(f'Disconnecting from >>> host: {self.host} port: {self.port}')
        self._socket_connection.close()
        self._socket_connection = None


    @property
    def _is_connected(self) -> bool:
        '''
        Checks if the TCP socket connection is active.

        Returns:
            bool: True if connected, False otherwise.
        '''

        return True if self._socket_connection else False
    
    def send_all(self, data: dict[str, dict[str, float]], message_size: int = 1024) -> None:
        '''
        Sends data to the server.

        Args:
            data (dict[str, dict[str, float]]): Data to be sent, formatted as a dictionary.

        Raises:
            Exception: If an error occurs while sending data.
        '''

        try:
            self.log.info('Serializing the object')
            serealized_object = pickle.dumps(data)

        except Exception as exception_message:
            self.log.critical('Unexpected error occured while serializing the object')
            self.log.error(exception_message)
            raise Exception

        if len(serealized_object) > message_size:
            self.log.warning('The package that you would like to send is begger that the buffer. Message will be split into multiple packages.')
            for index, chunk in enumerate(chunker(data=serealized_object, chunk_size=message_size)):
                self.log.info(f'Senidng chunk {index + 1}')
                self._socket_connection.sendall(chunk)

        else:
            self.log.info('Sending data to server')
            self._socket_connection.sendall(serealized_object)

        self.log.info('All messages been sent, nofying to server')
        self._socket_connection.sendall(b'!ALL_DATA_SENT')

        self._socket_connection.settimeout(0.5)
        self.log.info('Awaiting for the server response')
        serialized_message = self._socket_connection.recv(message_size)
        server_response = pickle.loads(serialized_message)
        
        if server_response == '!SUCCESS':
            self.log.debug(f'Server responded ... {server_response}')
            self.log.info('All data sent successfully')
        else:
            self.log.critical('Server did respond with !SUCCESS after receiving the message!')
            raise Exception

    def disconnect(self, disconnect_message: bytes = b'!DISCONNECT') -> None:
        '''
        Sends a disconnect message to the server.

        Args:
            disconnect_message (str): The message to be sent for disconnecting from the server.
        '''

        self.log.info('Sending disconnect message to server')
        self._socket_connection.sendall(disconnect_message)
        self.log.info('Disconnect message sent successfully')
