#!/usr/bin/env python3
import pandas
pandas.set_option('max_columns', None)

# excel_data_df = pandas.read_excel('records.xlsx', sheet_name='Employees')

def read_module():
    f_name = 'big_file/module_20220225.xlsx'
    r = dict()
    for sheet_name in pandas.ExcelFile(f_name).sheet_names:
        if sheet_name in ["目录", '变更记录']:
            continue
        df = pandas.read_excel(f_name, sheet_name=sheet_name)
        r[sheet_name] = df
    return r

module = read_module()

def search(s):
    for sheet_name, df in module.items():
        tname, colname = 1, 4
        tr = df.loc[df.iloc[:,tname]==s]
        cr = df.loc[df.iloc[:,colname]==s]
        
        print(tname, df)
        print('tr:', tr)        
        print('cr:', cr)
        break

search('实缴资本')


