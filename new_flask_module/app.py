#!/usr/bin/env python3

from csv import excel
from flask import jsonify,request
from lib_flask import app, Flask_url

# plan_old
# from table_json import json_context
# from flask_module.utils.mysql_utils import ReadMysql
# from utils.mysql_utils import ReadMysql
from flask_module.module import readMysql, colAppend, saveExcel  
from flask_module.code_maker import Code_maker

# plan
import copy
from new_flask_module.module.maker import plan_router_maker

# class home(Flask_url):
#     def init(self): 
#         self.data = [1,2,3]
#     def render(self):
#         print('render!')
#         return "<h1>codeloop.org, ID is {} </h1>".format(self.data)

# # class table(Flask_url):
# #     prefix = 'demo'
# #     def init(self):
# #         self.data = json_context
# #         self.set('name', 'table_info') 
# #     def post(self, params):
# #         # print('post params:', params)
# #         print('post get select_list:', params['select_list'], self.data['name'])
# #         return super().post(params)
# #     def render(self):
# #         print('render:select_list: ', self.data['select_list'])
# #         return jsonify(self.data)

# class module(Flask_url):
#     prefix = 'unit'
#     dynamic = ['db_table_name']
        
#     def get(self, db_table_name):
#         return jsonify(self.get_module())
#     def get_module(self, db_table_name):
#         print('db_table_name', db_table_name)
#         db_name, table_name = db_table_name.split('.')
#         module_info = dict(
#            db_table_name = db_table_name,
#            info = None
#         )
#         try:
#             rows = ReadMysql(f"test:test@127.0.0.1:3306/{db_name}")(
#                 f"SHOW FULL COLUMNS FROM {table_name}")
#             cols = "Field,Type,Collation,Null,Key,Default,Extra,Privileges,Comment".split(',')
#             field_list = [dict(zip(cols, row)) for row in rows]
#             rows = ReadMysql(f"test:test@127.0.0.1:3306/{db_name}")(
#                 f"""SELECT TABLE_SCHEMA,TABLE_NAME,TABLE_COMMENT,TABLE_CATALOG,TABLE_ROWS,AVG_ROW_LENGTH
#             FROM INFORMATION_SCHEMA.TABLES
#             WHERE TABLE_SCHEMA='{db_name}' and table_name='{table_name}';""")
#             cols = 'table_schema,table_name,table_comment,table_catalog,table_rows,avg_row_length'.split(',')
#             table_info = [dict(zip(cols, row)) for row in rows]
#             module_info['info'] = {
#                 'field_list':field_list,
#                 'table_info':table_info
#             }
#         except:
#             import traceback;print(traceback.format_exc())
#         return module_info

#     def post(self, module_info, db_table_name):
#         db_name, table_name = db_table_name.split('.')
#         self.set(db_table_name, module_info)
#         print('post!!', module_info)
#         try:
#             # create table
#             r = ReadMysql(f"test:test@127.0.0.1:3306/{db_name}")(module_info['info'].strip())
#             print('create module:', r)
#         except:
#             import traceback;print(traceback.format_exc())
#         return jsonify(self.data)

# class task(Flask_url):
#     prefix = 'unit'
#     dynamic = ['task_name']
#     def get(self, task_name):
#         task_info = self.data.get(task_name,
#             dict(
#                 task_name=task_name,
#                 src_list = [],
#                 out_name = 'out.xlsx',
#                 out_sheet = [
#                     dict(name='sheet1', fields=[]),
#                 ]
#             )
#         )
#         print('get: ret: task_info', task_info)
#         return jsonify(task_info)

#     def post(self, data, task_name):
#         self.set(task_name, data)
#         return None

# class task_src(module):
#     dynamic = ['src']
#     def get(self, src):
#         task_name, module_name = src.split('.', 1)
#         m = module().get_module(module_name)
#         return {'module':m, 'task':task_name}

class plan_old(Flask_url):
    dynamic = ['plan']
    
    def set_plan(self, plan, plan_copy):
        prev_fields = []
        # 计算每个functor的前置/后置fields
        for functor in plan_copy['functor_list']:
            functor.set_prev_fields(prev_fields)
            # functor.base_data['prev_fields'] = prev_fields
            prev_fields = functor.current_fields
        self.set(plan, plan_copy)

    def get(self, plan):
        if plan not in self.data:
            self.set_plan(plan, {
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
        plan_json = self.data[plan]
        functor_list = []
        for functor in plan_json['functor_list']:
            functor_list.append(functor.json_base)
        plan_json['functor_list'] = functor_list
        # print('plan_json', plan_json)
        return plan_json
    
    def post(self, data, plan):
        "{'key':'functor_list', 'idx':idx, 'data':data}"
        print("data", data)
        if data['method'].startswith('functor_'):
            functor = self.get_functor(plan, data['functor_id'])
            functor.op(**data)
            # print('functor_json', functor.json_base)
            self.set_functor(plan, data['functor_id'], functor)
        else:
            param = copy.deepcopy(data)
            del param['method']
            getattr(self, data['method'])(plan, **param)
        # 刷新，重产生prev_list
        self.set_plan(plan, self.data[plan])
        return {"error":'method_error'}
    
    def get_functor(self, plan, functor_id):
        plan_copy = self.data[plan]
        return plan_copy['functor_list'][functor_id]
    def set_functor(self, plan, functor_id, new_functor):
        plan_copy = self.data[plan]
        plan_copy['functor_list'][functor_id] = new_functor
        self.set_plan(plan, plan_copy)
    def functorNew(self, plan, functor_name):
        plan_copy = self.data[plan]
        functor_cls = eval(functor_name)
        plan_copy['functor_list'].append(functor_cls())
        self.set_plan(plan, plan_copy)
        print('new_functor', self.data[plan])
    def functorDel(self, plan, idx):
        plan_copy = self.data[plan]
        functor_list = plan_copy['functor_list']
        plan_copy['functor_list'] = functor_list[:idx] + functor_list[idx+1:]
        self.set_plan(plan, plan_copy)
    def make_code(self, plan):
        code = Code_maker(self.data[plan]).code
        with open('auto_code.py', 'w+') as f:
            f.write(code)
        plan_copy = self.data[plan]
        plan_copy['auto_code'] = code
        self.set_plan(plan, plan_copy)
    def save_plan(self, plan):
        plan_copy = self.data[plan]
        import pickle
        with open(f'flask_module/plan_lib/{plan}.pkl', 'wb') as f:
            pickle.dump(plan_copy, f)
    def load_plan(self, plan):
        plan_copy = dict()
        import pickle
        try:
            with open(f'flask_module/plan_lib/{plan}.pkl', 'rb') as f:
                plan_copy = pickle.load(f)
                # functor_list = plan_copy['functor_list']
                # for functor_data in functor_list:
                # for functor in plan_copy['functor_list']:
                #     functor.base_data['prev_fields'] = prev_fields
                #     prev_fields = functor.current_fields
                self.set_plan(plan, plan_copy)
        except:
            print(f'load plan [{plan}] fail!')
            import traceback;print(traceback.format_exc())

class plan(Flask_url):
    dynamic = ['plan_name']
    def init(self):
        pass
        # self.router = plan2_method_router 
    def get(self, plan_name):
        
        if plan_name not in self.data:
            print('plan_name', plan_name)
            self.set(plan_name, plan_router_maker(plan_name))
            print('self.data', self.data)

        r = self.data[plan_name].call([{
            'method': 'to_dict',
            # 'params': '',
        }])
        print('get ret:', r)
        return r
    def post(self, router_list, plan_name):
        self.data[plan_name].call(router_list)
    

if __name__ == "__main__":
    
    # home.registry(app)
    # # table.registry(app)
    # module.registry(app)
    # task.registry(app)
    # task_src.registry(app)
    plan_old.registry(app)
    plan.registry(app)
    app.run(debug=True)


    """
export PYTHONPATH=`pwd`;python new_flask_module/app.py

python new_flask_module/module/plan.py > /home/chd/demo/next_demo/pages/plan2/libs/base_module.js
"""



