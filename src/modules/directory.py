from pathlib import Path

from models.no_dir_exception import DirNotCreateException

def create_direcotry(path: Path) -> None:
    '''
    Create a directory at the specified path if it does not already exist.

    Args:
        path (Path): The path where the directory should be created.

    Raises:
        OSError: If an operating system error occurs during directory creation.
        ValueError: If the given path is invalid.
        Exception: For any other exception that occurs during directory creation.
        DirNotCreateException: If the directory is not created after the attempt.
    '''

    if path.resolve().exists():
        return
    
    try:
        path.mkdir(parents=True)
    except OSError:
        raise OSError
    except ValueError:
        raise ValueError
    except Exception:
        raise Exception
    else:
        if not path.exists():
            raise DirNotCreateException(path=path.as_posix())