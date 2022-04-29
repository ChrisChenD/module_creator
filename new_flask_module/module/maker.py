from lib_flask import app, Flask_url
# from utils.mysql_utils import ReadMysql
# from module import readMysql, colAppend, saveExcel  
import copy
from new_flask_module.module.plan import Plan

# 我们设计一个方法路由的东西
class Method_router:
    class Method:
        def __init__(self, obj, router):
            self.obj = obj
            self.router = router
        def next_obj(self):
            # {
            #     'method':func_name,
            #     'params':[params]
            # }
            # print('self.router', self.router)
            # print('obj', dir(self.obj))
            
            func = getattr(self.obj, self.router['method'])
            params = self.router.get('params', None)
            if params is not None:
                return func(**params)
            return func()
            # return getattr(self.obj, self.router['method'])(
            # )

    def __init__(self, root_obj):
        self.root_obj = root_obj
    def call(self, router_list):
        obj = self.root_obj
        for router in router_list:
            assert isinstance(router, dict)
            print('router', router)
            obj = Method_router.Method(obj, router).next_obj()
        ret = obj
        return ret

plan_router_maker = lambda plan_name:Method_router(Plan(name=plan_name))
