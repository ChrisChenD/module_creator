#!/usr/bin/env python3

# import pandas
# pandas.set_option('max_columns', None)
import pickle

def string_to_table(py_string = 'mysql.db143.sq_fin_procfnew_tmp'):
    method, db_name, table_name = py_string.split('.')
    module = None
    with open('big_file/data_module.pkl', 'rb') as f:
        module = pickle.load(f)

    table_list = module[db_name]
    table = [table for table in table_list if table['table_name']==table_name][0]
    # print('find table:')
    # print(table)
    # print(table.keys())
    return table



#     for table in db:
#         tname, tcname = table['table_name'], table["table_cn"]
#         cols, data = table['cols'], table['data']


# for db_name, db in module.items():
#     if db_name == 'db152':
        