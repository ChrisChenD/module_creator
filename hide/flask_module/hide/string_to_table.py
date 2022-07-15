#!/usr/bin/env python3

# import pandas
# pandas.set_option('max_columns', None)
from multiprocessing import ProcessError
import pickle

class Table:
    def __init__(self, table_module):
        self.module = table_module
        self.tb_name = self.module['table_name']
        self.tb_cname = self.module['table_cn']
        # self.cols = self.module['cols']
        # self.samples = ''
        self.cols = [dict(
            name=col['name'],
            cname=col['cname'] if len(col['cname'])<10 else col['cname'][:10]+' ...',
            type=col['type']
            )
            for col in self.module['cols']
        ]
        self.select = []
        self.cond = []
        self.add_default()
    def add_default(self):
        self.select = [True]*len(self.cols)
        self.cond = ['']*len(self.cols)
        for i,col in enumerate(self.cols):
            if col == 'dataStatus':
                self.cond[i] = 'dataStatus!=3'
            if col == 'isValid':
                self.cond[i] = 'isValid=1'
            if col in ['id', 'dataStatus', 'isValid', 'modifyTime', 'createTime']:
                self.select[i] = False
    @property
    def info(self):
        return dict(
            tb_name=self.tb_name,
            tb_cname=self.tb_cname,
            cols=self.cols,
            select=self.select,
            cond=self.cond
        )
    @info.setter
    def info(self, new_info):
        self.tb_name=new_info['tb_name']
        self.tb_cname=new_info['tb_cname']
        self.cols=new_info['cols']
        self.select=new_info['select']
        self.cond=new_info['cond']
    
            # print('table_info:', table)
            # cols = [dict(
            #     name=col['name'],
            #     cname=col['cname'] if len(col['cname'])<10 else col['cname'][:10]+' ...',
            #     type=col['type']
            #     )
            #     for col in table['cols']
            # ]
            # return dict(
            #     tb_name=table['table_name'],
            #     tb_cname = table['table_cn'],
            #     cols=cols,
                
            # )

class Data_module:
    def get_module(self):
        module = None
        with open('big_file/data_module.pkl', 'rb') as f:
            module = pickle.load(f)
        return module    
    def list_db(self):
        module = self.get_module()
        return list(module.keys())
    def list_table(self, db_name):
        module = self.get_module()
        table_list = module[db_name]
        return [tb['table_name'] for tb in table_list]
    def get_table(self, db_name, table_name):
        module = self.get_module()
        table_list = module[db_name]
        for table in table_list:
            if table['table_name'] == table_name:
                return Table(table)
                # return table_parse(table)
        return None
    
    # def set_table(self, task, resource)

data_module = Data_module()


def string_to_table(py_string = 'mysql.db143.sq_fin_procfnew_tmp'):
    method, db_name, table_name = py_string.split('.')
    return data_module.get_table(db_name, table_name)
    # # module = None
    # # with open('big_file/data_module.pkl', 'rb') as f:
    # #     module = pickle.load(f)

    # table_list = module[db_name]
    # table = [table for table in table_list if table['table_name']==table_name][0]
    # # print('find table:')
    # # print(table)
    # # print(table.keys())
    # return table



#     for table in db:
#         tname, tcname = table['table_name'], table["table_cn"]
#         cols, data = table['cols'], table['data']


# for db_name, db in module.items():
#     if db_name == 'db152':



