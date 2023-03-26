class DBData:
    __conf = {
        "username": "",
        "password": "",
        "MYSQL_PORT": 3306,
        "MYSQL_DATABASE": 'mydb',
        "MYSQL_DATABASE_TABLES": ['tb_users', 'tb_groups']
    }
    __setters = ["username", "password"]

    @staticmethod
    def config(name):
        return DBData.__conf[name]

    @staticmethod
    def set(name, value):
        if name in DBData.__setters:
            DBData.__conf[name] = value
        else:
            raise NameError("Name not accepted in set() method")
