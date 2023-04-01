from mysql_wrap import Database
from db_structure import TbInfo




class DatabaseTb(Database):
    def __init__(self, host_name: str, user: str, user_passwd: str, db_name: str):
        super().__init__(host_name, user, user_passwd, db_name)

    def insert_dbinfo_in_table(self, tb_info = TbInfo):
        """/////"""

        table_name = TbInfo.get_tb_name()
        column_data = TbInfo.get_all_cols()

        return super().insert_into_table(table_name, column_data)