#!/usr/bin/env python3
# 1 读取表 + select + cond
# 2 field_append
# 3 row-map
# 4 col-filter
# 5 write_to_excel_sheet1
from modulefinder import Module

class Table:
    class chain:
        def __init__(self, host_port, usr_pwd, db, tb) -> None:
            self.host_port = host_port
            self.usr_pwd = usr_pwd
            self.db = db
            self.tb = tb
        @property
        def string(self):
            host,port,usr,pwd = [*self.host_port, *self.usr_pwd]
            return f'{usr}:{pwd}@{host}:port/{self.db}'

class Module_maker:
    def __init__(self) -> None:
        self.db_dict = dict()
    def add_tab(self, s):
        s = s.split('\n')
        s = ' '*4+(' '*4+'\n').join(s)
        return s
    def add(self, db, tb):
        if db not in self.db_dict:
            self.db_dict[db] = []
        self.db_dict[db].append(tb)
    def db_str(self, db_name):
        table_list = self.db_dict[db_name]
        table_cls = lambda tb_name,db_name : f'class {tb_name}(Table):db_name = "{db_name}"'
        table_list = [table_cls(table, db_name) for table in table_list]
        table_list = '\n'.join(table_list)
        r = f"""
class {db_name}:
{self.add_tab(table_list)}
        """.rstrip()
        return r 
    def __str__(self):
        db_list = list(self.db_dict.keys())
        db_list = '\n'.join([self.db_str(db_name) for db_name in db_list])
        r = f"""
class module:
{self.add_tab(db_list)}
        """.strip()
        return r
    @staticmethod
    def test():
        module = Module_maker()
        module.add('db136_sydb', "dwd_ms_cn_px_list")
        module.add('db136_sydb', "dwd_ms_cn_px_invo_info")
        module.add('db136_dbsy', "dwd_mm_cn_smjj_info")
        print(module)
# class module:
#     class db136_sydb:
#         class dwd_ms_cn_px_list(Table):db_name = "db136_sydb"
#         class dwd_ms_cn_px_invo_info(Table):db_name = "db136_sydb"
#     class db136_dbsy:
#         class dwd_mm_cn_smjj_info(Table):db_name = "db136_dbsy"


# class Functors:
#     def _1_read_table(table_chain, ):
#         r = f"""
#         df = ReadMysql()
        
#         """.strip()


if __name__ == '__main__':
    Module_maker.test()


