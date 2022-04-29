#!/usr/bin/env python3
import copy
from new_flask_module.module.mysql_utils import ReadMysql
from new_flask_module.module.module_base import js_maker, Module_common
from new_flask_module.module.compo import Com

cls1 = 'bg-stone-700 border-4 text-white'

@js_maker.registry()
class New_functor(Module_common):
    members__ = {
        'name':'New_functor',
        'data':None
    }
    def init(self, **kwargs):
        self.data = Com.P(cls1, kwargs['name'])
        
    def access__(self): return Plan.get_functor_new

    def set_trigger(self, add_functor):
        self.add_functor_trigger = add_functor
        return self
    @js_maker.registry_call('New_functor', [])# , is_router=True)
    def add_functor(self):
        self.add_functor_trigger(self.name)


@js_maker.registry()
class Plan_op(Module_common):
    members__ = {
        'name':'Plan_op',
        'data':Com.Line(cls1, [
            Com.P(cls1, '推送代码到git'),
            Com.P(cls1, '运行命令'),
        ])
# // <p>:推送代码到git</p>
# // <p>:运行命令</p>
    }

@js_maker.registry()
class Plan(Module_common):
    members__ = {
        'name':'plan',
        'functor_list':[],
        'new_functor_list':[],
        'op':Plan_op()
    }
    def add_functor(self, func_name):
        self.functor_list.append(eval(func_name)())
    def init(self, **kwargs):
        # f = New_functor(name='readMysql')
        # f = f.set_trigger(self.add_functor)
        self.new_functor_list = [
            New_functor(name='readMysql').set_trigger(self.add_functor),
            # f,
            New_functor(name='colAppend').set_trigger(self.add_functor),
            New_functor(name='saveExcel').set_trigger(self.add_functor),
        ]
    # default__ = {}
    @js_maker.registry_router('Plan', ['functor_id'])# , is_router=True)
    # @js_maker.registry_call(['functor_id'])
    def get_functor(self, functor_id):
        return self.functor_list[functor_id]
    @js_maker.registry_router('Plan', ['functor_id'])# , is_router=True)
    # @js_maker.registry_call(['functor_id'])
    def get_functor_new(self, functor_id):
        return self.new_functor_list[functor_id]
    

@js_maker.registry()
class Functor(Module_common):
    def access__(self): return Plan.get_functor
    # @staticmethod
    # def ___access():
    #     return Plan2.get_functor
    # def ___access(self): return Plan2.get_functor
    ### 我们已经验证了, 增加一个路由/直接调用接口能够成功
    
    # >>> 现在正在验证 access 机制， access 在类的一开始, 声明该类, 属于哪个类的子类
    # >>> 以及如何进入
    # .>. 我们考虑, 在 access里面, 只声明父类, 以及方法
    # >> 明天考虑系统性的重构我们的这次工程, 我们这波重构, 
    #     >>>> 期待能够在假期到达之前完整的完成
    # >>> ....


@js_maker.registry()
class MysqlFunctor(Functor):
    @js_maker.registry_call('MysqlFunctor', ['field_id'])
    def select_switch(self, field_id):
        # self.base_data['select_list'].select_switch(field_id)
        pass

    @js_maker.registry_call('MysqlFunctor', ['field_id', 'cond'])
    def modify_cond(self, field_id, cond):
        # cond_line = self.base_data['cond_list']
        # cond_line.set(cond_line._real_id(field_id), cond)
        pass
    
    @property
    def field_list(self):
        db_name, table_name = self.db_name, self.table_name
        field_list = []
        try:
            rows = ReadMysql(f"test:test@127.0.0.1:3306/{db_name}")(
                f"SHOW FULL COLUMNS FROM {table_name}")
            cols = "Field,Type,Collation,Null,Key,Default,Extra,Privileges,Comment".split(',')
            field_list = [
                dict(zip(cols, row)) for row in rows
            ]
        except:
            import traceback;print(traceback.format_exc())
        return field_list

    @property
    def table_info(self):
        db_name, table_name = self.db_name, self.table_name
        table_info = []
        try:
            rows = ReadMysql(f"test:test@127.0.0.1:3306/{db_name}")(
                f"""SELECT TABLE_SCHEMA,TABLE_NAME,TABLE_COMMENT,TABLE_CATALOG,TABLE_ROWS,AVG_ROW_LENGTH
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_SCHEMA='{db_name}' and table_name='{table_name}';"""
            )
            cols = 'table_schema,table_name,table_comment,table_catalog,table_rows,avg_row_length'.split(',')
            table_info = [dict(zip(cols, row)) for row in rows][0]
        except:
            import traceback;print(traceback.format_exc())
        return table_info
    
    def init_base_data(self):
        print('init_base_data!')

@js_maker.registry()
class readMysql(MysqlFunctor):
    def load_chain(self, db_chain) -> None:
        self.db_name, self.table_name = db_chain.split(".")
        self.init_base_data()

@js_maker.registry()
class saveExcel(Functor):
    def load_chain(self, db_chain) -> None:
        # self.base_data['db_chain'] = db_chain
        self.db_chain = db_chain

@js_maker.registry()
class colAppend(MysqlFunctor):
    ""
    # def item_map(self):
    #     from module_lines import item_map2
    #     return item_map2(self.field_list)
    def load_chain(self, db_chain) -> None:
        self.db_name, self.table_name = db_chain.split(".")
        self.init_base_data()

    def select_chunk_key(self, field_id):
        # self.base_data['prev_list'].select_chunk_key(field_id)
        # self.prev_list.select_chunk_key(field_id)
        pass
    
    def set_append_key(self, field_id):
        # self.base_data['append_key'] = self.base_data['select_list'][field_id]
        self.append_key = self.select_list[field_id]
    def set_root_key(self, prev_id):
        # self.base_data['prev_root_key'] = self.base_data['prev_fields'][prev_id]
        self.prev_root_key = self.prev_fields[prev_id]


if '__main__' == __name__:
    # print(Plan2.to_javascript())
    # print(Plan2.sons)
    print(js_maker.code)
    # print(Plan2.get_functor.link__)
    # 1 树结构: 我们假设页面就是这样
    # 2 复用, 我们增加一个类型继承

    # 在对应的类里面, 产生了对应的调用方法
    ## 但是我其实不需要, 
    # 本地产生一个调用参数, 怎么产生?
    # 参考产生 js 的代码

    # 



