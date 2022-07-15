#!/usr/bin/env python3

#!/usr/bin/env python3
import copy
from os import supports_effective_ids
from turtle import onclick
from module.module_base import Module_base, Module_root, module_info
# 普通的类/叶子节点继承 Module_base
# 作为模型根节点 继承 Module_root
# from module.compo import Com, Module_base_debug
# debug的叶子节点, 继承 Module_base_debug
# 这个效果是自动给类分配一个内容(类的名字), 用来观察
from module.compo.compo_canvas import Com_canvas as Com
from plan_flask.module.functor.functor import pandas_king

# for add_functor
# from plan_flask.module.mvc_functor import ReadMysqlDb,ColAppend,SaveExcel
# from plan_flask.module.mvc_functor import ReadMysqlDb_Table,Table2
from plan_flask.module.code_maker.code_gen import code_gen
from plan_flask.module.functor.functor import pandas_king

cls1 = 'bg-stone-700 border-4 text-white'


# @module_info.registry
# class NewFunctor(Module_base):
#     @staticmethod
#     def m(): return dict(
#         name=Com.Com_Button
#     )
#     def init(self, functor_name):
#         self.name.init(functor_name, 
#             onClick=[
#                 # 'self.root.functor_list.add_functor',
#                 self.root.functor_list.idx,
#                 'add_functor',
#                 dict(functor_name=functor_name)
#             ],
#         cls_name=cls1)


# @module_info.registry
# class Plan_op(Module_base):
#     @staticmethod
#     def m(): return dict(
#         region_name=Com.Com_P,
#         plan_op_list = Com.Com_Line,
#         code = Com.Com_textarea
#     )
#     def init(self):
#         self.region_name.init('REGION:OP')
#         self.plan_op_list.init(e_list = [
#             # Com.Com_
#             # Com.Com_P(self, 'ReadMysql'),
#             Com.Com_Button(self, 'SAVE_PLAN', onClick=[
#                 self.root.idx,
#                 'SAVE_MODULE',
#                 dict()
#             ]),
#             Com.Com_Button(self, 'LOAD_PLAN', onClick=[
#                 self.root.idx,
#                 'LOAD_MODULE',
#                 dict()
#             ]),
            
#             Com.Com_Button(self, 'CODE_GENERATE', onClick=[
#                 # self.idx,
#                 self.root.canvas.idx,
#                 'CODE_GENERATE',
#                 dict()
#             ]),
#             Com.Com_Button(self, 'CODE_PUSH', onClick=[
#                 self.idx,
#                 'CODE_PUSH',
#                 dict()
#             ]),
#         ])
#         self.code.init('code',rown=30, coln=60)
#         # code = Com.Com_textarea
#     # def codeEnter(self, text):
#     #     self.code.text = text
#     # def CODE_GENERATE(self):
#     #     print('Plan_op:CODE_GENERATE!!!!')
#     #     self.code.text = code_gen(self.root.functor_list.functor_list.e_list)        
#     def SET_CODE(self, code):
#         print('set_code', code)
#         self.code.init(code)
#         print('self.code', self.code)
#     def CODE_PUSH(self):
#         # self.code.text = code_gen(self.root.functor_list.functor_list.e_list)        
#         self.CODE_GENERATE()
#         import os
#         plan_name = self.root.name
#         with open(f'/home/ubuntu/git/robot_code/auto/{plan_name}.py', 'w+') as f:
#             f.write(self.code.text)
#         print('code: push!!!!')
#         os.system("cd /home/ubuntu/git/robot_code;git add .;git commit -m '.';git push")
#         print('code: push ok!!!!')
        

# @module_info.registry
# class Plan_functors(Module_base):
#     @staticmethod
#     def m(): return dict(
#         region_name=Com.Com_P,
#         functor_list=Com.Com_List,
#     )
#     def init(self):
#         self.region_name.init('REGION:Functors')
#         self.functor_list.init(e_list=[
#         ])
#     def add_functor(self, functor_name):
#         functor = eval(functor_name)(self)
#         functor.init()
#         self.functor_list.e_list.append(functor)
#     def prev_field_list(self, functor_idx):
#         fields = []
#         for functor in self.functor_list.e_list:
#             if functor.idx == functor_idx:
#                 break
#             fields = functor.out_fields(fields)
#         return fields
        
#         # return []
    


# @module_info.registry
# class Plan_new_functors(Module_base):
#     @staticmethod
#     def m(): return dict(
#         region_name=Com.Com_P,
#         functor_list=Com.Com_List,
#     )
#     def init(self):
#         self.region_name.init('REGION:New_functors')
#         self.functor_list.init(e_list=[
#             NewFunctor(self, 'ReadMysqlDb'),
#             NewFunctor(self, 'ColAppend'),
#             NewFunctor(self, 'SaveExcel'),
#         ])


@module_info.registry
class Plan(Module_root):
    @staticmethod
    def m():
        return dict(
            plan_name=Com.Com_P,
            op_line=Com.Com_Line,
            add_functor_line=Com.Com_Line,
            functor_op_line=Com.Com_Line,
            # canvas=Com.Com_Canvas,
            canvas=Com.Com_Graph,
            cur_functor=Com.Com_List,
            code=Com.Com_textarea,
            # op=Plan_op,
            # functor_list=Plan_functors,
            # new_functor_list=Plan_new_functors,
        )
    def SET_CODE(self, code):
        # print('set_code', code)
        self.code.init(code)
        # print('self.code', self.code)
    def init(self, plan_name):
        self.name = plan_name
        self.plan_name.init(value=f'Poc计划: {plan_name}')#  = Com.Com_P(self, name)# = name
        self.op_line.init(e_list = [
            Com.Com_Button(self, '操作任务', 
                cls_name=cls1
            ),
            Com.Com_Button(self, '任务存档', onClick=[
                self.root.idx,
                'SAVE_MODULE',
                dict()
            ]),
            Com.Com_Button(self, '任务读取', onClick=[
                self.root.idx,
                'LOAD_MODULE',
                dict()
            ]),
            
            Com.Com_Button(self, '产生代码', onClick=[
                self.root.canvas.idx,
                'CODE_GENERATE',
                dict()
            ]),
        ])
        
        self.add_functor_line.init([
            Com.Com_Button(self, '引入算子', 
                cls_name=cls1
            ),
        ]+[
            Com.Com_Button(self.add_functor_line,
                value=genus_cn, 
                onClick=[
                    self.root.canvas.idx,
                    'render_genus',
                    dict(genus_name=genus_name)
                ]
            )
            for genus_name,genus_cn in pandas_king.genus_name_list()
        ])
        
        self.functor_op_line.init([
            Com.Com_Button(self, '操作算子', 
                cls_name=cls1
            ),
            Com.Com_Button(self, '删除选中算子', 
                onClick=[
                    self.root.canvas.idx,
                    'del_highlight_functor',
                    dict()
                ],
                cls_name=cls1
            ),
            Com.Com_Button(self, '连接算子', 
                onClick=[
                    self.root.canvas.idx,
                    'set_link_bind',
                    dict()
                ],
                cls_name=cls1
            ),
            Com.Com_Button(self, '取消连接', 
                onClick=[
                    self.root.canvas.idx,
                    'set_link_unbind',
                    dict()
                ],
                cls_name=cls1
            ),
        ])

        # w,h = Com.Com_Graph.graph_level_wh(Com.Com_Graph.levelRoot)
        # self.canvas.canvas_w = w*1.2
        # self.canvas.canvas_h = h*1.2
        # offset_xy = w*0.1,h*0.1
        # offset_y = h*0.1
        
        # module=Genus_base(
        #     cn='模块',
        #     species_dict=dict(
        # def init(self, spec_id, name, offset, level,
        self.canvas.init(
            spec_id = pandas_king.make_spec_id(
                'module','F_CustomModule'
            ),
            name='main',
            offset=dict(x=0,y=0),
            level=0,
            graph_functor_list=[],
            graph_link_table={}
        ),
        # 设置canvas参数

        self.cur_functor.init([])
        self.code.init('code',rows=100, cols=80)

    
    
    


