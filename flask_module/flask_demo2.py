#!/usr/bin/env python3

import json
from logging import exception
from re import L
from sys import prefix
from unicodedata import name
from flask import jsonify,request
from lib_flask import app, Flask_url
from table_json import json_context
from flask_module.utils.mysql_utils import ReadMysql
from module import Module

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

class Functor:
    def __init__(self, name, chain='not_define_chain'):
        self.name = name
        self.chain = chain
    def to_dict(self):
        r = dict()
        for member_name in dir(self):
            if not member_name.startswith('_'):
                member = getattr(self)
                if not callable(member):
                    r[member_name] = member
        return r
    

class plan(Flask_url):
    dynamic = ['plan']
    # def init(self):
    #     self.data = dict()
    def get(self, plan):
        # task_name, module_name = src.split('.', 1)
        # m = module().get_module(module_name)
        if plan not in self.data:
            self.set(plan, {
                'name':plan, 
                'functor_list':[
                    {'name':'read_mysql'},
                ],
                'new_functor_list':[
                    # 1 读取表 + select + cond
                    # 2 field_append
                    # 3 row-map
                    # 4 col-filter
                    # 5 write_to_excel_sheet1
                    {'name':'read_mysql'},
                    {'name':'col_append'},
                    {'name':'col_map'},
                    {'name':'row_filter'},
                    {'name':'save_excel'},
                ],
                'op':[],
            })
        return self.data[plan]
        # // task.name
        # // functor_list
        # // new_functor_list
        # // task.op
    def post(self, data, plan):
        "{'key':'functor_list', 'idx':idx, 'data':data}"
        plan_copy = self.data[plan]
        new_plan = getattr(self, data['method'])(plan_copy, **data)
        self.set(plan, new_plan)
        return {'plan':new_plan}
    
    def functor_add_chain(self, plan_copy, functor_idx, db_chain):
        # m = module().get_module(db_chain)
        functor = plan_copy['functor_list'][functor_idx]
        # this.name = data.name//string
        # this.idx = data.idx
        # this.table_info = data.table_info
        db,tb = db_chain.split('.')
        module = Module(db, tb)
        functor['table_info'] = module.table_info
        plan_copy['functor_list'][functor_idx] = functor
        return plan_copy
        # {
        #     "name": module.table_info['table_name'],
        # # this.name = data.name//string
        # # this.name_ext = data.name_ext
        # # this.fields = data.fields
        # }
        # Module

    def functor_new(self, plan_copy, name, **kwargs):
        plan_copy['functor_list'].append(
            {'name':name}
        )
        return plan_copy
    def functor_del(self, plan_copy, idx, **kwargs):
        functor_list = plan_copy['functor_list']
        plan_copy['functor_list'] = functor_list[:idx] + functor_list[idx+1:]
        return plan_copy
    


if __name__ == "__main__":
    home.registry(app)
    table.registry(app)
    module.registry(app)
    task.registry(app)
    task_src.registry(app)
    plan.registry(app)
    app.run(debug=True)

    # r = home().get('abc')
    # print(r)



