import unittest
from datetime import datetime
from modules.date import get_time

class TestGetTime(unittest.TestCase):
    def test_get_time_format(self):
        '''
        Test if the returned time string has the correct format.
        '''
        time_format = '%Y_%m_%d_%H_%M_%S'
        current_time = get_time()
        try:
            datetime.strptime(current_time, time_format)
        except ValueError:
            self.fail(f'Time "{current_time}" does not match the format "{time_format}".')

    def test_get_time_type(self):
        '''
        Test if the return value is a string.
        '''
        current_time = get_time()
        self.assertIsInstance(current_time, str, 'Return value is not a string.')

if __name__ == '__main__':
    unittest.main()