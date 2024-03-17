import platform

def get_file_name(path: str) -> str:
    '''
    Extract the file name from the given path.

    Args:
        path (str): The path of the file.

    Returns:
        str: The extracted file name without the file extension.
    '''
    
    file_name = path.split('\\')[-1] if platform.system() == 'Windows' else path.split('/')[-1]
    return file_name[:file_name.index('.')] if '.' in file_name else file_name
