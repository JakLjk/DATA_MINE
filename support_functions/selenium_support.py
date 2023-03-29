from time import sleep


# TODO try passing logging as argument, if not passed - user does not want to log 
def driver_connection_retry(driver, 
                            url, 
                            retry_intervals: list, 
                            raise_error = True, 
                            logging = None):
    
    connection_established = False
    for i, interval in enumerate(retry_intervals):
        try: 
            driver.get(url)
            connection_established = True
            break
        except:
            if logging: # TODO check type logging == logging
                logging.error(f'Exception webriver get method raised')
                logging.error(f"Retry {i+1} / {len(retry_intervals)}, In {interval} seconds")
            sleep(interval)
    if connection_established == False: 
        if raise_error: raise Exception(f"Unable to connect to url {url} ")
        else: return None