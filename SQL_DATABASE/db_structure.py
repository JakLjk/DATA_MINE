
class TbInfo:
    """////"""
    def __init__(self, table_name:str="", 
                 table_insert_data:dict={}) -> None:
        assert table_name != "", "Table name cannot be empty"

        self.__table_name = table_name
        self.__tb_insert_data = table_insert_data

    @classmethod
    def pass_table_info(cls, 
                        table_name:str = "",
                        table_column_names:list = []):
        
        return cls(table_name, 
                   {key:None for key in table_column_names})
        
    def set_col(self):
        pass

    def get_col(self):
        pass

    def get_all_cols(self) -> dict:
        pass

    def get_tb_name(self) -> str:
        pass


    

# TODO add this for Liskov's principle sake 
    
class TbInfoGet:
    #
    pass

class TbInfoSet:
    pass

class TbInfoManage:
    #
    pass