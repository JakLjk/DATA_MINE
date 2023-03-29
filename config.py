class DBConf:
    __conf = {

        "username": "localhost",
        "password": "root",

        "MYSQL_PORT": 0000,
        "MYSQL_HOSTNAME": 'localhost',
        "MYSQL_DBNAME": "houses_data"
        # "MYSQL_DATABASE_TABLES": ['', '']
    }
    __setters = ["username", "password"]

    @staticmethod
    def config(name):
        return DBConf.__conf[name]

    @staticmethod
    def set(name, value):
        if name in DBConf.__setters:
            DBConf.__conf[name] = value
        else:
            raise NameError("Name not accepted in set() method")
        
class DriverConf:
    HEADLESS = True
    WAIT_UNTIL_PAGE_LOADED = 1.6
    ANTI_THROTTLE_WAIT = 4
    THROTTLE_REPEATS = [10,30,45,90,120]
    SITE_LOAD_SCROLL_PAUSETIME = 0.05
    SITE_LOAD_AFTER_SCROLL_PAUSETIME = 1.2

class LoggingConf:
    LOG_FILE_PATH_NAME = ""

class DataManiConf:
    CLEAR_LINKS = True
    GET_PARSED_BEFORE_AGAIN = False




