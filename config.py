class DBConf:
    """Standard db configuration parameters,
    Which can be changed / added when program is iniialised"""
    __conf = {

        "username": "root",
        "password": "",

        "MYSQL_PORT": None,
        "MYSQL_HOSTNAME": 'localhost',
        "MYSQL_DBNAME": "houses_data"
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

class LoggingConf:
    """Path for logging file"""
    LOG_FILE_PATH_NAME = ""


class Misc:
    FunctionRetries = 3



