from dataclasses import dataclass

@dataclass
class Argument:
    '''
    Base dataclass representing common arguments.
    '''
    
    ticker: str
    log_level: str

@dataclass
class ScrapperArgument(Argument):
    '''
    Dataclass representing arguments for the scrapper.
    '''

    report_range: str

@dataclass
class ClientArgument(Argument):
    '''
    Dataclass representing arguments for the client.
    '''

    server: str
    port: str