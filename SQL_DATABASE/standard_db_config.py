class DBConf:
    """Standard db configuration parameters,
    Which can be changed / added when program is iniialised"""
    __conf = {

        "username": "root",
        "password": "",
        "database_name": "",

        
        "SQL_HOSTNAME": 'localhost',
        "SQL_PORT": None,
    }
    __setters = ["username", "password", "database_name"]

    @staticmethod
    def config(name):
        return DBConf.__conf[name]

    @staticmethod
    def set(name, value):
        if name in DBConf.__setters:
            DBConf.__conf[name] = value
        else:
            raise NameError("Name not accepted in set() method")
    
    # Used in situation, where it has to be pointed out, that improper
    # credentials were given, or weren't given at all
    class CredentialsError():
        pass
        
