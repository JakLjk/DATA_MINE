from time import sleep
from logger import logger

def function_retry(function, 
                    args, 
                    retries: list or int, 
                    raise_error = True):
    """Retries function based on given values,
    can retry function specified amoutn of times instantly,
    or given list of arguments (in seconds) can retry function in given intervals"""

    connection_established = False
    if isinstance(retries, int):
        retries = range(retries)

    for i, interval in enumerate(retries):
        try: 
            if isinstance(args, tuple):
                f = function(*args)
            else:
                f = function(args)
            connection_established = True
            return f
        except Exception as e:
            logger.error(f'Error has occured while executing function {function.__name__}')
            logger.error(f"Raised exception: {e}")

            if isinstance(retries, list):
                logger.error(f"Retry {i+1} / {len(retries)}, In {interval} seconds")
                sleep(interval)
            else:
                logger.error(f"Retry {i+1} / {len(retries)}")

    if connection_established == False: 
        if raise_error: raise Exception(f"Unable to execute function: {function.__name__} ")
        else: return None