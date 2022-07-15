#!/usr/bin/env python3
import pickle
import pandas
pandas.set_option('max_columns', None)


module = None
with open('big_file/data_module.pkl', 'rb') as f:
    module = pickle.load(f)

tab = ' '*4
print('## ')
print('from module_common import Db, Table, Column')
print('import pandas, datetime')
print('nan, NaT = [None,]*2')
print('class mysql:')
for db_name, db in module.items():
    pre_tab = tab
    print(pre_tab+f'class {db_name}(Db):')

    for table in db:
        tname, tcname = table['table_name'], table["table_cn"]
        cols, data = table['cols'], table['data']
        def have_substrs(name, substr_list):
            for substr in substr_list:
                if substr in name:
                    return True
            return False
        # 异常数据过滤:
        def is_good(c):
            name = c['name']
            if have_substrs(name, [
                'PRIMARY','UNIQUE','KEY', 
                ]): 
                return False
            return True
        path = f"mysql.{db_name}.{tname}"
        if path in [
            'mysql.db135.sy_sa_zxyh_ms_cn_comp_geo_loc_list_data',
        ]:# 这个表有字段叫做 'GDB(2019)', 跳过这个表
            continue
        cols_raw = ','.join([col['name'] for col in cols if is_good(col)])
        pre_tab = tab*2
        print(pre_tab+f'class {tname}(Table):')
        pre_tab = tab*3

        print(pre_tab+f'@property')
        print(pre_tab+f'def _db(self): ')
        pre_tab = tab*4
        print(pre_tab+f"if '_db' not in self.kwargs: self.kwargs['_db'] = mysql.{db_name}()")
        print(pre_tab+f"return self.kwargs['_db']")
        pre_tab = tab*3
        print(pre_tab+f'_path = "{path}"')# 用来eval
        print(pre_tab+f'_cname = "{tcname}"')
        print(pre_tab+f'_sample = {data[0] if len(data)>0 else dict()}')
        print(pre_tab+f'_cols = "{cols_raw}"')
        
        for col in cols:
            name, cname, vtype = col['name'], col['cname'], col['type']
            if not is_good(col):
                continue
            pre_tab = tab*3
            print(pre_tab+f'class {name}(Column):')
            pre_tab = tab*4
            print(pre_tab+f'@property')
            print(pre_tab+f'def _table(self):')
            pre_tab = tab*5
            print(pre_tab+f"if '_table' not in self.kwargs: self.kwargs['_table'] = mysql.{db_name}.{tname}(**self.kwargs)")
            print(pre_tab+f"return self.kwargs['_table']")
            pre_tab = tab*4

            print(pre_tab+f'_path = "mysql.{db_name}.{tname}.{name}"')# 用来eval
            print(pre_tab+f'_cname = "{cname}"')
            print(pre_tab+f'_vtype = "{vtype}"')
        
    #     break
    # break
"""
./pymodule_creator.py > big_file/mysql_pymodule.py
"""
# 
