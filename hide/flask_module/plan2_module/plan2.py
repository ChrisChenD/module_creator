from lib_flask import app, Flask_url
# from utils.mysql_utils import ReadMysql
from module import readMysql, colAppend, saveExcel  
import copy
from plan2_module.module_plan2 import Plan2

# 我们设计一个方法路由的东西
class Method_router:
    class Method:
        def __init__(self, obj, router):
            self.obj = obj
            self.router = router
        def next_obj(self):
            return getattr(self.obj, self.router['method'])(
                self.router['params']
            )
    def __init__(self, root_obj):
        self.root_obj = root_obj
    def call(self, router_list):
        obj = self.root_obj
        for router in router_list:
            assert isinstance(router, dict)
            obj = Method_router.Method(obj, router).next_obj()
        ret = obj
        return ret

plan_router_maker = lambda plan_name:Method_router(Plan2(plan_name))


# class plan(Flask_url):
#     dynamic = ['plan']
#     def set_plan(self, plan, plan_copy):
#         prev_fields = []
#         # 计算每个functor的前置/后置fields
#         for functor in plan_copy['functor_list']:
#             functor.set_prev_fields(prev_fields)
#             # functor.base_data['prev_fields'] = prev_fields
#             prev_fields = functor.current_fields
#         self.set(plan, plan_copy)

#     def get(self, plan):
#         if plan not in self.data:
#             self.set_plan(plan, {
#                 'name':plan,
#                 'functor_list':[
#                     # {'name':'read_mysql'},
#                 ],
#                 'new_functor_list':[
#                     # 1 读取表 + select + cond
#                     # 2 field_append
#                     # 3 row-map
#                     # 4 col-filter
#                     # 5 write_to_excel_sheet1
#                     {'name':cls_.__name__}
#                     for cls_ in [readMysql, colAppend, saveExcel]
#                 ],
#                 'op':[],
#             })
#         plan_json = self.data[plan]
#         functor_list = []
#         for functor in plan_json['functor_list']:
#             functor_list.append(functor.json_base)
#         plan_json['functor_list'] = functor_list
#         # print('plan_json', plan_json)
#         return plan_json
    
#     def post(self, data, plan):
#         "{'key':'functor_list', 'idx':idx, 'data':data}"
#         print("data", data)
#         if data['method'].startswith('functor_'):
#             functor = self.get_functor(plan, data['functor_id'])
#             functor.op(**data)
#             # print('functor_json', functor.json_base)
#             self.set_functor(plan, data['functor_id'], functor)
#         else:
#             param = copy.deepcopy(data)
#             del param['method']
#             getattr(self, data['method'])(plan, **param)
#         # 刷新，重产生prev_list
#         self.set_plan(plan, self.data[plan])
#         return {"error":'method_error'}
    