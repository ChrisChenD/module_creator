#!/usr/bin/env python3

import json
from logging import exception
from sys import prefix
from flask import jsonify,request
from lib_flask import app, Flask_url
from table_json import json_context
from flask_module.utils.mysql_utils import ReadMysql


class home(Flask_url):
    def init(self): 
        self.data = [1,2,3]
    def render(self):
        print('render!')
        return "<h1>codeloop.org, ID is {} </h1>".format(self.data)

class table(Flask_url):
    prefix = 'demo'
    def init(self):
        self.data = json_context
        self.set('name', 'table_info') 
    def post(self, params):
        # print('post params:', params)
        print('post get select_list:', params['select_list'], self.data['name'])
        return super().post(params)
    def render(self):
        print('render:select_list: ', self.data['select_list'])
        return jsonify(self.data)

# home.registry(lambda f:f)

#run flask app

# /unit/create_module/db152.xxx
class module(Flask_url):
    prefix = 'unit'
    dynamic = ['db_table_name']
        
    def get(self, db_table_name):
        return jsonify(self.get_module())
    def get_module(self, db_table_name):
        print('db_table_name', db_table_name)
        db_name, table_name = db_table_name.split('.')
        module_info = dict(
           db_table_name = db_table_name,
           info = None
        )
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
        return module_info

    def post(self, module_info, db_table_name):
        db_name, table_name = db_table_name.split('.')
        self.set(db_table_name, module_info)
        # data = self.data
        # data[db_table_name] = module_info
        # self.data = data
        print('post!!', module_info)
        try:
            # create table
            r = ReadMysql(f"test:test@127.0.0.1:3306/{db_name}")(module_info['info'].strip())
            print('create module:', r)
        except:
            import traceback;print(traceback.format_exc())
        return jsonify(self.data)

class task(Flask_url):
    prefix = 'unit'
    dynamic = ['task_name']
    # task_info.task_name = 'xxx'
    # task_info.src_list = [src, ...src],
    # task_info.out_name = 'xxx'
    # task_info.out_sheet = [
    #     sheet = {
    #     name = '',
    #     fields = [field, ...field]
    #     }    
    # ]
    def get(self, task_name):
        task_info = self.data.get(task_name,
            dict(
                task_name=task_name,
                src_list = [],
                out_name = 'out.xlsx',
                out_sheet = [
                    dict(name='sheet1', fields=[]),
                ]
            )
        )
        print('get: ret: task_info', task_info)
        return jsonify(task_info)

    def post(self, data, task_name):
        self.set(task_name, data)
        return None

class task_src(module):
    dynamic = ['src']
    def get(self, src):
        task_name, module_name = src.split('.', 1)
        m = module().get_module(module_name)
        return {'module':m, 'task':task_name}
    

if __name__ == "__main__":
    home.registry(app)
    table.registry(app)
    module.registry(app)
    task.registry(app)
    task_src.registry(app)
    app.run(debug=True)

    # r = home().get('abc')
    # print(r)



