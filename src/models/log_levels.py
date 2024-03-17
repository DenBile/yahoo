from enum import Enum

class LogLevel(Enum):
    '''
    Enum representing different log levels.
    '''
        
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'
