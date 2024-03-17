def chunker(data: bytes, chunk_size: int):
    '''
    Generator function to yield chunks of data with a specified chunk size.
    
    Args:
        data (bytes): The data to be chunked.
        chunk_size (int): The size of each chunk.
        
    Yields:
        bytes: Chunks of data with the specified chunk size.
    '''

    if chunk_size <= 0:
        raise ValueError
    
    total_chunks = (len(data) + chunk_size - 1) // chunk_size
    
    for i in range(total_chunks):
        start = i * chunk_size
        end = min(start + chunk_size, len(data))
        
        yield data[start:end]