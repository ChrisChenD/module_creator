#!/usr/bin/env python3

#!/usr/bin/env python3
import copy
# from new_flask_module.module.mysql_utils import ReadMysql
# from new_flask_module.module.module_base import js_maker, Module_common
# from new_flask_module.module.compo import Com
from module.module_base import Module_base
from module.compo import Com
cls1 = 'bg-stone-700 border-4 text-white'
# from module_creator.mvc_flask.module.compo import Com

class Module_info:
    def __init__(self):
        self.cls_list = []
    def registry(self, class_):
        self.cls_list.append(class_)
        return class_
module_info = Module_info()



@module_info.registry
class NewFunctor(Module_base):
    def init(self, functor_name):
        self.name = Com.p(self, functor_name, cls_name=cls1)
        # self.name = functor_name
    
    @staticmethod
    def m(): return dict(
        name=Com.p
    )
    @classmethod
    def v(cls_):
        m = cls_.m()
        return m['name'].v()

@module_info.registry
class ReadMysql(Module_base):
    # def m(self):
    pass
@module_info.registry
class SaveExcel(Module_base):
    # def m(self):
    pass

@module_info.registry
class ColAppend(Module_base):
    # def m(self):
    pass

@module_info.registry
class Plan_op(Module_base):
    pass

@module_info.registry
class Plan(Module_base):
    def default_module(plan_name='for_js'):
        return Plan(None, name=plan_name)# root=None

    @staticmethod
    def m():
        return dict(
            name=Com.p,
            functor_list=Com.List,
            new_functor_list=Com.List,
            op=Com.p
        )
    def init(self, name):
        self.name = name
        self.functor_list = []
        self.new_functor_list = [
            NewFunctor(self, 'ReadMysql'),
            NewFunctor(self, 'ColAppend'),
            NewFunctor(self, 'SaveExcel'),
            # ReadMysql(self),
            # ColAppend(self),
            # SaveExcel(self)
        ]
        self.op = Plan_op(self)
    @classmethod
    def v(cls_):
        return f"""
            <div {cls_.base_attr()}>
                <h1>Plan {{self.name}}</h1>
                {{self.functor_list.map(
                    (functor, idx)=>{{
                        return <p>functor</p>
                    }}
                )}}
                {{self.new_functor_list.map(
                    (functor, idx)=>{{
                        return <NewFunctor.view {{...functor}}></NewFunctor.view>
                    }}
                )}}
            </div>
        """.strip()

