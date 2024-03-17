from abc import ABC, abstractclassmethod

class TCPSocket(ABC):

    def __enter__(self):
        '''
        Allows to use "with" keyword to establish connection against the server.

        Returns:
            self: TCPSocket object.
        '''
        
        self._connect()
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        '''
        Closes the connection against the server.
        '''

        if any( (exception_type, exception_value, traceback) ):
            self.log.error(f'Disconnected from the database due to an unexpected exception ...')
            self.log.error(f'Exception type: {exception_type}')
            self.log.error(f'Exception value: {exception_value}')
            self.log.error(f'Traceback: {traceback}')
        self._disconnect()

    @abstractclassmethod
    def _connect(self) -> None:
        '''
        Establishes a connection with the server.
        '''

        pass
        
    @abstractclassmethod
    def _disconnect(self) -> None:
        '''
        Closes the connection with the server.
        '''

        pass
