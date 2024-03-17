from enum import Enum

class ReportRanges(Enum):
    '''
    Enum defining different report ranges.
    '''
        
    ONE_MONTH = '1mo'
    TWO_MONTHS = '2mo'
    THREE_MONTHS = '3mo'
    SIX_MONTHS = '6mo'
    YEAR = '12mo'
    TWO_YEARS = '24mo'
    MAX = 'max'
