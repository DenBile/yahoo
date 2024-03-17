import pickle
import socket

from modules.logger import Logger
from modules.socket.tcp import TCPSocket


class TCPServer(TCPSocket):
    '''
    Class for managing TCP socket connections.
    '''


    def __init__(self, log: Logger, host: str, port: int, max_connections: int = 10) -> None:
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

        self.max_connections = max_connections
        self._socket_connection = None

    def _connect(self) -> None:
        '''
        Establishes a connection with the server.
        '''

        try:
            self.log.info(f'Opening connection >>> host: {self.host} port: {self.port}')
            self._socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket_connection.bind((self.host, self.port))
            self._socket_connection.listen(self.max_connections)

        except socket.error as error:
            self.log.critical('Exception occured while opening a connection')
            self.log.error(error)

            if self._socket_connection:
                self._socket_connection.close()
            raise Exception
        
        except Exception as exception_message:
            self.log.critical('Unexpected exception occured while opening a connection')
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
    
    def accept_messages(self, message_size: int = 1024, disconnect_message: bytes = b'!DISCONNECT') -> None:
        '''
        Accepts messages on the server side.

        Args:
            message_size (int, optional): The size of the message buffer. Defaults to 1024.
            message_format (str, optional): The encoding format of the message. Defaults to 'utf-8'.
            disconnect_message (bytes, optional): The message indicating disconnection. Defaults to b'!DISCONNECT'.

        Raises:
            Exception: If an error occurs while receiving or processing messages.`
        '''

        if not self._is_connected:
            self.log.warning('No connection established, no message will be accepted')
            return

        disconnect = False
        while not disconnect:
            received_messages = []

            self.log.info('Accepting messages on server side')
            communication_socket, address = self._socket_connection.accept()
            self.log.info(f'Connected to {address}')

            while True:
                serialized_message = communication_socket.recv(message_size)

                if serialized_message == disconnect_message:
                    disconnect = True
                    break
                    
                self.log.debug(f'Message received: {serialized_message}')
                received_messages.append(serialized_message)
            
                if serialized_message.endswith(b'!ALL_DATA_SENT'):
                    received_messages_in_bytes = b''.join(received_messages)
                    message = pickle.loads(received_messages_in_bytes[: -len(b'!ALL_DATA_SENT')])

                    self.log.info(f'Message from client is: {message}')
                    received_messages = []

                    communication_socket.send(pickle.dumps('!SUCCESS'))

        self.log.info('No further messages will be accepted from the server side')
        communication_socket.close()
        self._socket_connection = None
        self.log.info(f'Connection with {address} ended')