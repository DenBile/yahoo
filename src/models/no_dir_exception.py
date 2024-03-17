class DirNotCreateException(Exception):
    '''
    Exception raised when unable to create a directory.
    
    Args:
        path (str): The path of the directory.
    '''

    def __init__(self, path: str) -> None:
        '''
        Initializes the exception with the given directory path.
        
        Args:
            path (str): The path of the directory.
        '''
        
        super().__init__(f'Unable to create directory: {path}')