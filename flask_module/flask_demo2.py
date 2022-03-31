#!/usr/bin/env python3

import json
from logging import exception
from sys import prefix
from flask import jsonify,request
from lib_flask import app, Flask_url
from table_json import json_context
from flask_module.utils.mysql_utils import ReadMysql


class home(Flask_url):
    def __init__(self):
        self.params = [1,2,3]
    def render(self):
        print('render!')
        return "<h1>codeloop.org, ID is {} </h1>".format(self.params)

class table(Flask_url):
    prefix = 'demo'
    def __init__(self):
        self.params = json_context
        self.params['name'] = 'table_info'
    # def get(self):
    #     # print('get select_list:', self.params['select_list'], self.params['name'])
    #     return super().get()
    def post(self, params):
        # print('post params:', params)
        print('post get select_list:', params['select_list'], self.params['name'])
        return super().post(params)
    def render(self):
        print('render:select_list: ', self.params['select_list'])
        return jsonify(self.params)

# home.registry(lambda f:f)

#run flask app

# /unit/create_module/db152.xxx
class module(Flask_url):
    prefix = 'unit'
    dynamic = ['db_table_name']
    def __init__(self):
        self.params = {}
    # def render(self):
    #     return f"{self.params['db_table_name']}.{self.params['table_name']}"
    def get(self, db_table_name):
        print('db_table_name', db_table_name)
        db_name, table_name = db_table_name.split('.')
        module_info = dict(
           db_table_name = db_table_name,
           info = None
        )
        # if db_table_name in self.params:
        #     module_info = self.params[db_table_name]
        try:
            rows = ReadMysql(f"test:test@127.0.0.1:3306/{db_name}")(
                f"SHOW FULL COLUMNS FROM {table_name}")
            cols = "Field,Type,Collation,Null,Key,Default,Extra,Privileges,Comment".split(',')
            field_list = [dict(zip(cols, row)) for row in rows]
            # print('info_list', info_list)
            # table comment
            # comment,catalog,rows_num,avg_rowlen
            rows = ReadMysql(f"test:test@127.0.0.1:3306/{db_name}")(
                f"""SELECT TABLE_SCHEMA,TABLE_NAME,TABLE_COMMENT,TABLE_CATALOG,TABLE_ROWS,AVG_ROW_LENGTH
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA='{db_name}' and table_name='{table_name}';""")
            cols = 'table_schema,table_name,table_comment,table_catalog,table_rows,avg_row_length'.split(',')
            table_info = [dict(zip(cols, row)) for row in rows]
            # print('db_name,table_name,TABLE_COMMENT,TABLE_CATALOG,TABLE_ROWS,AVG_ROW_LENGTH', comment,catalog,rows_num,avg_rowlen)
            # print('r', r)
            module_info['info'] = {
                'field_list':field_list,
                'table_info':table_info
            }
            # WHERE TABLE_SCHEMA='db152' and table_name='sy_cd_ms_base_gs_comp_info_new';
        except:
            import traceback;print(traceback.format_exc())

        # print('get!!', module_info)
        return jsonify(module_info)

    def post(self, module_info, db_table_name):
        db_name, table_name = db_table_name.split('.')
        self.params[db_table_name] = module_info
        print('post!!', module_info)
        try:
            # create table
            r = ReadMysql(f"test:test@127.0.0.1:3306/{db_name}")(module_info['info'].strip())
            print('create module:', r)
        except:
            import traceback;print(traceback.format_exc())
        
        return jsonify(self.params)

class task(Flask_url):
    prefix = 'unit'
    dynamic = ['task_name']
    def __init__(self):
        self.params = {}
        # task_info.task_name = 'xxx'
        # task_info.src_list = [src, ...src],
        # task_info.out_name = 'xxx'
        # task_info.out_sheet = [
        #     sheet = {
        #     name = '',
        #     fields = [field, ...field]
        #     }    
        # ]
    # def render(self):
    #     return f"{self.params['db_table_name']}.{self.params['table_name']}"
    def get(self, task_name):
        task_info = self.params.get(task_name,
            dict(
                task_name=task_name,
                src_list = [],
                out_name = 'out.xlsx',
                out_sheet = [
                    dict(name='sheet1', fields=[]),
                ]
            )
        )
        return jsonify(task_info)

    def post(self, data, task_name):
        self.params[task_name] = data
        return None

class task_src(module):
    pass

if __name__ == "__main__":
    home.registry(app)
    table.registry(app)
    module.registry(app)
    task.registry(app)
    task_src.registry(app)
    app.run(debug=True)

    # r = home().get('abc')
    # print(r)



