#!/usr/bin/env python3

#!/usr/bin/env python3
import copy
from turtle import onclick
from module.module_base import Module_base, Module_root, module_info
# 普通的类/叶子节点继承 Module_base
# 作为模型根节点 继承 Module_root
from module.compo import Com, Module_base_debug
# debug的叶子节点, 继承 Module_base_debug
# 这个效果是自动给类分配一个内容(类的名字), 用来观察

# for add_functor
from mvc_flask.module.mvc_functor import ReadMysqlDb,ColAppend,SaveExcel
from mvc_flask.module.mvc_functor import ReadMysqlDb_Table,Table2
from mvc_flask.module.code_maker.code_gen import code_gen


cls1 = 'bg-stone-700 border-4 text-white'


@module_info.registry
class NewFunctor(Module_base):
    @staticmethod
    def m(): return dict(
        name=Com.Com_Button
    )
    def init(self, functor_name):
        self.name.init(functor_name, 
            onClick=[
                # 'self.root.functor_list.add_functor',
                self.root.functor_list.idx,
                'add_functor',
                dict(functor_name=functor_name)
            ],
        cls_name=cls1)


@module_info.registry
class Plan_op(Module_base):
    @staticmethod
    def m(): return dict(
        region_name=Com.Com_P,
        plan_op_list = Com.Com_Line,
        code = Com.Com_textarea
    )
    def init(self):
        self.region_name.init('REGION:OP')
        self.plan_op_list.init(e_list = [
            # Com.Com_
            # Com.Com_P(self, 'ReadMysql'),
            Com.Com_Button(self, 'SAVE_PLAN', onClick=[
                self.root.idx,
                'SAVE_MODULE',
                dict()
            ]),
            Com.Com_Button(self, 'LOAD_PLAN', onClick=[
                self.root.idx,
                'LOAD_MODULE',
                dict()
            ]),
            
            Com.Com_Button(self, 'CODE_GENERATE', onClick=[
                self.idx,
                'CODE_GENERATE',
                dict()
            ]),
            Com.Com_Button(self, 'CODE_PUSH', onClick=[
                self.idx,
                'CODE_PUSH',
                dict()
            ]),
        ])
        self.code.init('code',rown=30, coln=60)
        # code = Com.Com_textarea
    # def codeEnter(self, text):
    #     self.code.text = text
    def CODE_GENERATE(self):
        self.code.text = code_gen(self.root.functor_list.functor_list.e_list)        
    def CODE_PUSH(self):
        # self.code.text = code_gen(self.root.functor_list.functor_list.e_list)        
        self.CODE_GENERATE()
        import os
        plan_name = self.root.name
        with open(f'/home/ubuntu/git/robot_code/auto/{plan_name}.py', 'w+') as f:
            f.write(self.code.text)
        print('code: push!!!!')
        os.system("cd /home/ubuntu/git/robot_code;git add .;git commit -m '.';git push")
        print('code: push ok!!!!')
        

@module_info.registry
class Plan_functors(Module_base):
    @staticmethod
    def m(): return dict(
        region_name=Com.Com_P,
        functor_list=Com.Com_List,
    )
    def init(self):
        self.region_name.init('REGION:Functors')
        self.functor_list.init(e_list=[
        ])
    def add_functor(self, functor_name):
        functor = eval(functor_name)(self)
        functor.init()
        self.functor_list.e_list.append(functor)
    def prev_field_list(self, functor_idx):
        fields = []
        for functor in self.functor_list.e_list:
            if functor.idx == functor_idx:
                break
            fields = functor.out_fields(fields)
        return fields
        
        # return []
    


@module_info.registry
class Plan_new_functors(Module_base):
    @staticmethod
    def m(): return dict(
        region_name=Com.Com_P,
        functor_list=Com.Com_List,
    )
    def init(self):
        self.region_name.init('REGION:New_functors')
        self.functor_list.init(e_list=[
            NewFunctor(self, 'ReadMysqlDb'),
            NewFunctor(self, 'ColAppend'),
            NewFunctor(self, 'SaveExcel'),
        ])


@module_info.registry
# class Plan(Module_base, Module_root)
class Plan(Module_root):
    @staticmethod
    def m():
        return dict(
            plan_name=Com.Com_P,
            functor_list=Plan_functors,
            new_functor_list=Plan_new_functors,
            op=Plan_op
        )
    def init(self, plan_name):
        self.name = plan_name
        self.plan_name.init(value=f'PLAN: {plan_name}')#  = Com.Com_P(self, name)# = name
        self.functor_list.init()
        self.new_functor_list.init()
        self.op.init()
    # def CODE_GENERATE(self):
    #     print('CODE_GENERATE!!!')
    
    
    


