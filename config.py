class DBConf:
    __conf = {
        "username": "",
        "password": "",
        "MYSQL_PORT": 0000,
        "MYSQL_DATABASE": '',
        "MYSQL_DATABASE_TABLES": ['', '']
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

class Links:
    MAIN_LINK  = "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/slaskie?distanceRadius=0&market=ALL&locations=%5Bregions-12%5D&viewType=listing"
    PARSED_MAIN_LINK = "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/slaskie?distanceRadius=0&market=ALL&locations=%5Bregions-12%5D&viewType=listing&page={}"
    LINK_MAIN_PART  = "https://www.otodom.pl{}"



