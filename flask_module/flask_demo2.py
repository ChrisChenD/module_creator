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
from module import readMysql, colAppend, saveExcel  

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

# class Functor:
#     def __init__(self, name, chain='not_define_chain'):
#         self.name = name
#         self.chain = chain
#     def to_dict(self):
#         r = dict()
#         for member_name in dir(self):
#             if not member_name.startswith('_'):
#                 member = getattr(self)
#                 if not callable(member):
#                     r[member_name] = member
#         return r
    

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
                    # {'name':'read_mysql'},
                ],
                'new_functor_list':[
                    # 1 读取表 + select + cond
                    # 2 field_append
                    # 3 row-map
                    # 4 col-filter
                    # 5 write_to_excel_sheet1
                    {'name':cls_.__name__}
                    for cls_ in [readMysql, colAppend, saveExcel]
                ],
                'op':[],
            })
        # print("self.data[plan]", self.data[plan])
        # return jsonify(self.data[plan])
        plan_json = self.data[plan]
        # print('plan_json', plan_json)
        functor_list = []
        for functor in plan_json['functor_list']:
            # print('functor', functor)
            functor_list.append(functor.json_base)
        plan_json['functor_list'] = functor_list
        # return self.data[plan]
        # print('get data:', plan_json)
        return plan_json
        # // task.name
        # // functor_list
        # // new_functor_list
        # // task.op
    def post(self, data, plan):
        "{'key':'functor_list', 'idx':idx, 'data':data}"
        print("data", data)
        if data['method'].startswith('functor_'):
            functor = self.get_functor(plan, data['functor_id'])
            functor.op(**data)
            # print('functor_json', functor.json_base)
            self.set_functor(plan, data['functor_id'], functor)
        else:
            getattr(self, data['method'])(plan, **data)
            # return self.functor_op(plan, **data)
        # pass
        # plan_copy = self.data[plan]
        # import copy
        # kwargs = copy.deepcopy(data)
        # del kwargs['method']
        # # del kwargs['table_name']
        # new_plan = getattr(self, data['method'])(plan_copy, **kwargs)
        # print('post', data)
        # self.set(plan, new_plan)
        # return {'plan':new_plan}
        return {"error":'method_error'}
    # def select_switch(self, plan_copy, functor_idx, field_idx):
    #     # 'field_idx':index,
    #     # 'functor_idx':idx
    #     functor = plan_copy['functor_list'][functor_idx]
    #     functor['select_list'][field_idx] = not functor['select_list'][field_idx]
    #     plan_copy['functor_list'][functor_idx] = functor
    #     return plan_copy
    
    def get_functor(self, plan, functor_id):
        plan_copy = self.data[plan]
        return plan_copy['functor_list'][functor_id]
    def set_functor(self, plan, functor_id, new_functor):
        plan_copy = self.data[plan]
        plan_copy['functor_list'][functor_id] = new_functor
        self.set(plan, plan_copy)
        # return plan_copy['functor_list'][functor_id]
    # def append_functor(self, plan)

    # def functor_op(self, plan, functor_id, **kwargs):
    #     functor.op(**kwargs)
    #     # import copy
    #     # kwargs = copy.deepcopy(data)
    #     # del kwargs['method']
    #     # del kwargs['table_name']
    #     db,tb = module_chain.split('.')
    #     # Module(db, tb)
    #     plan_copy = self.data[plan]
    #     new_plan = getattr(self, method)(plan_copy, **kwargs)
    #     # print('post', data)
    #     self.set(plan, new_plan)
    #     return {'plan':new_plan}

    # def functor_add_chain(self, plan_copy, functor_idx, db_chain):
    #     functor = self.get_functor(plan_copy, functor_idx)
        
        # functor = plan_copy['functor_list'][functor_idx]
        # # print('db_chain', db_chain)
        # db,tb = db_chain.split('.')
        # functor = Module(db, tb).maker_functor_ext(functor)
        # plan_copy['functor_list'][functor_idx] = functor
        # print('plan_copy', plan_copy.keys())
        # return plan_copy

    def functorNew(self, plan, functor_name, method):
        plan_copy = self.data[plan]
        functor_cls = eval(functor_name)
        plan_copy['functor_list'].append(functor_cls())
        # self.data[plan] = plan_copy
        self.set(plan, plan_copy)
        print('new_functor', self.data[plan])
        # return plan_copy
    def functorDel(self, plan, idx, method):
        plan_copy = self.data[plan]
        functor_list = plan_copy['functor_list']
        plan_copy['functor_list'] = functor_list[:idx] + functor_list[idx+1:]
        # plan_copy['functor_list'].append(functor_cls())
        self.set(plan, plan_copy)
        # self.data[plan] = plan_copy
        # return plan_copy
    

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



