from time import sleep

class RetryFailure(Exception):
    pass

# TODO add retry only for specified exception
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
            if isinstance(retries, list):
                sleep(interval)


    if connection_established == False: 
        if raise_error: raise RetryFailure(f"Unable to execute function: {function.__name__} ")
        else: return None