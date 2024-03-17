from datetime import datetime, timezone

def get_time() -> str:
    '''
    Get the current UTC time in the format 'YYYY_MM_DD_HH_MM_SS'.

    Returns:
        str: A string representing the current UTC time.
    '''
    
    time_now = datetime.now(tz=timezone.utc)
    current_time = time_now.strftime('%Y_%m_%d_%H_%M_%S')
    return current_time