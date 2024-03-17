import unittest
from modules.chunker import chunker

class TestChunker(unittest.TestCase):

    def test_chunker_with_exact_chunk_size(self):
        # Test with data length divisible by chunk size
        data = b'abcdefghij'
        chunk_size = 5
        expected_chunks = [b'abcde', b'fghij']
        self.assertEqual(list(chunker(data, chunk_size)), expected_chunks)

    def test_chunker_with_remainder(self):
        # Test with data length not divisible by chunk size
        data = b'abcdefghijk'
        chunk_size = 5
        expected_chunks = [b'abcde', b'fghij', b'k']
        self.assertEqual(list(chunker(data, chunk_size)), expected_chunks)

    def test_chunker_with_single_chunk(self):
        # Test with chunk size larger than data length
        data = b'abcdefg'
        chunk_size = 10
        expected_chunks = [b'abcdefg']
        self.assertEqual(list(chunker(data, chunk_size)), expected_chunks)

    def test_chunker_with_empty_data(self):
        # Test with empty data
        data = b''
        chunk_size = 5
        expected_chunks = []
        self.assertEqual(list(chunker(data, chunk_size)), expected_chunks)

    def test_chunker_with_zero_chunk_size(self):
        # Test with zero chunk size
        with self.assertRaises(ValueError):
            chunk_size = 0
            list(chunker(b'abcdefghij', chunk_size))

    def test_chunker_with_negative_chunk_size(self):
        # Test with negative chunk size
        with self.assertRaises(ValueError):
            chunk_size = -5
            list(chunker(b'abcdefghij', chunk_size))

if __name__ == '__main__':
    unittest.main()