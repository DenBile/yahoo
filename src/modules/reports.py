import pandas as pd
from pathlib import Path
from dataclasses import dataclass, field

from .directory import create_direcotry

from .logger import Logger


@dataclass(slots=True)
class Report:
    '''
    A custom class for managing reports and Excel files.
    '''

    log: Logger
    dir: Path
    ticker: str

    _file_name: str = field(init=False)
    _excel_path: str = field(init=False)

    def __post_init__(self) -> None:
        '''
        Initializes the Report object after it has been created.
        '''
        
        self._file_name = f'{self.ticker}.xlsx'
        self._excel_path = f'{self.dir.as_posix()}/{self._file_name}'
    
    @property
    def file_exists(self):
        '''
        Checks if the Excel file already exists.

        Returns:
            bool: True if the file exists, False otherwise.
        '''

        return Path(self._excel_path).resolve().is_file()

    def create_new_excel_file(self, data: pd.DataFrame) -> None:
        '''
        Creates a new Excel file with the provided DataFrame.

        Args:
            data (pd.DataFrame): DataFrame containing the data to be written to the Excel file.

        Raises:
            IOError: If an I/O error occurs while creating the Excel file.
            Exception: For any other unexpected exception that occurs.
        '''

        create_direcotry(path=self.dir)

        try:
            self.log.info('Creating Excel file for the report')
            with pd.ExcelWriter(path=self._excel_path, engine='openpyxl') as writer:
                data.to_excel(writer, sheet_name=f'{self.ticker}_history', index=True)
        except IOError:
            self.log.critical('IOError occured while creating Excel file')
            raise IOError
        except Exception as exception_message:
            self.log.critical('Unexpected exception occured while creating Excel file')
            self.log.error(exception_message)
            raise Exception
        else:
            self.log.info('Wrote data successfully to a file.')
    
    def open_existing_excel_file(self) -> pd.DataFrame:
        '''
        Opens an existing Excel file and returns its content as a DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing the data from the Excel file.

        Raises:
            IOError: If an I/O error occurs while opening the Excel file.
            Exception: For any other unexpected exception that occurs.
        '''

        try:
            self.log.info('Opening file with historical data')
            with pd.ExcelFile(self._excel_path) as xls_reader:
                df_historical_data = pd.read_excel(xls_reader, sheet_name=f'{self.ticker}_history')
            
            if not df_historical_data.empty:
                df_historical_data = df_historical_data.set_index('Date')

        except IOError:
            self.log.critical('IOError occured while opening Excel file')
            raise IOError
        except Exception as exception_message:
            self.log.critical('Unexpected exception occured while opening Excel file')
            self.log.error(exception_message)
            raise Exception
        else:
            self.log.info('Excel file with historical data opened successfully')
            self.log.debug(f'\n{df_historical_data}')
        
        return df_historical_data

    def extend_excel_file(self, data: pd.DataFrame) -> None:
        '''
        Extends an existing Excel file with new data.

        Args:
            data (pd.DataFrame): DataFrame containing the data to be added to the Excel file.

        Raises:
            IOError: If an I/O error occurs while extending the Excel file.
            Exception: For any other unexpected exception that occurs.
        '''

        try:
            self.log.info('Extending Excel file for the report')
            with pd.ExcelWriter(path=self._excel_path, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                data.to_excel(writer, sheet_name=f'{self.ticker}_history', index=True)
        except IOError:
            self.log.critical('IOError occured while extending Excel file')
            raise IOError
        except Exception as exception_message:
            self.log.critical('Unexpected exception occured while extending Excel file')
            self.log.error(exception_message)
            raise Exception
        else:
            self.log.info('Wrote data successfully to a file.')
    