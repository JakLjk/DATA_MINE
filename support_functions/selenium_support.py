from time import sleep
from logger import logger

# TODO try passing logging as argument, if not passed - user does not want to log 
def driver_connection_retry(driver, 
                            url, 
                            retry_intervals: list, 
                            raise_error = True):
    
    connection_established = False
    for i, interval in enumerate(retry_intervals):
        try: 
            print(url)
            driver.get(url)
            connection_established = True
            break
        except:
            logger.error(f'Exception webriver get method raised')
            logger.error(f"Retry {i+1} / {len(retry_intervals)}, In {interval} seconds")
            sleep(interval)
    if connection_established == False: 
        if raise_error: raise Exception(f"Unable to connect to url {url} ")
        else: return None