#!/usr/bin/env python3
import copy
from module.module_base import Module_base, Module_root, module_info
# 普通的类/叶子节点继承 Module_base
# 作为模型根节点 继承 Module_root
from module.compo import Com, Module_base_debug
from mvc_flask.module.mysql_lib.mysql_module import Mysql_module
from mvc_flask.module.mvc_functor_table import ReadMysqlDb_Table, Table2
from mvc_flask.module.mvc_functor_table import cls_select


# debug的叶子节点, 继承 Module_base_debug
# 这个效果是自动给类分配一个内容(类的名字), 用来观察

cls1 = 'bg-stone-700 border-4 text-white'

class Functor_base(Module_base):
    def prev_fields(self):
        return self.root.functor_list.prev_field_list(self.idx)
    def out_fields(self, prev_fields):
        out_fields = prev_fields
        return prev_fields

@module_info.registry
class ReadMysqlDb(Functor_base):
    @staticmethod
    def m(): 
        return dict(
            src_info=Com.Com_Line,
            table=ReadMysqlDb_Table
        )
    def init(self):
        self.src_info.init(e_list=[
            Com.Com_P(self, value='FUNCTOR:ReadMysqlDb'),
            Com.Com_text(self, text='', 
            onEnter=[
                self.table.idx,
                'load_module',
                dict()
            ]),
        ])
        self.table.init('db_aliyun.sy_cd_ms_sh_gs_shlist_new')
    def out_fields(self, prev_fields):
        return self.table.out_fields()
    def param_for_code(self):
        return self.table.param_for_code()

@module_info.registry
class SaveExcel(Functor_base):
    @staticmethod
    def m(): 
        return dict(
            excel_info=Com.Com_Line,
            prev_fields_select=Com.Com_Line,
        )
    def init(self):
        self.excel_name = 'default'
        self.prev_field_list = self.prev_fields()
        self.rename_list = copy.deepcopy(self.prev_field_list)

        self.build_module(self.excel_name)
    def rename_list_set(self, text, idx):
        print('text', text)
        print('idx', idx)
        self.rename_list[idx] = text
        self.build_module(self.excel_name)

    def build_module(self, text=''):
        self.excel_name = text
        self.excel_info.init(e_list=[
            Com.Com_P(self, value='Excel:'),
            Com.Com_text(self, text=self.excel_name, 
            onEnter=[
                self.idx,
                'init_excel_info',
                dict()
            ]),
        ])
        self.prev_fields_select.init(e_list=[
            Com.Com_Line(self, e_list=[
                Com.Com_P(self, value=field),
                Com.Com_text(self, text=self.rename_list[i],
                    onEnter=[
                        self.idx,
                        'rename_list_set',
                        dict(idx=i)
                    ]
                )
            ])
            for i,field in enumerate(self.prev_field_list)
        ])

    def param_for_code(self):
        # self.table.param_for_code()
        excel_name = self.excel_name
        rename_dict = dict([
            (field, field)
            for field in self.prev_field_list
        ])
        return (
            excel_name, rename_dict
        )


@module_info.registry
class ColAppend(Functor_base):
    @staticmethod
    def m(): 
        return dict(
            src_info=Com.Com_Line,
            table=Table2,
            prev_fields_select=Com.Com_Line,
        )
    def init(self):
        ''
        self.src_info.init(e_list=[
            Com.Com_P(self, value='FUNCTOR:ReadMysqlDb'),
            Com.Com_text(self, text='', 
            onEnter=[
                self.table.idx,
                'load_module',
                dict()
            ]),
        ])
        self.table.init('db_aliyun.sy_cd_ms_sh_gs_shlist_new')
        self.build_prev_fields()

    def build_prev_fields(self, prev_key_idx=0):
        self.prev_field_list = self.prev_fields()
        # self.rename_list = copy.deepcopy(self.prev_field_list)
        # self.prev_field_list = ['prev_field1', 'prev_field2']
        self.prev_key_idx = prev_key_idx
        self.prev_fields_select.init(e_list=[
            Com.Com_Line(self, e_list=[
                Com.Com_Button(self, 
                value=field if field else '__',
                    onClick=[
                        self.idx,
                        'select_prev_key',
                        dict(key_idx=idx-1)
                    ],
                    cls_name=self.cls_name_gen_prev(idx)
                )
            ])
            for idx,field in enumerate(['SELECT:prev_fields']+self.prev_field_list)
        ])
    def select_prev_key(self, key_idx):
        # print('select_prev_key:', key_idx)
        # self.prev_key_idx = key_idx
        self.build_prev_fields(key_idx)

    def prev_key(self): 
        return self.prev_field_list[self.prev_key_idx]
    def cls_name_gen_prev(self, idx):
        return cls_select(self.prev_key_idx == idx-1)

    def param_for_code(self):
        param = self.table.param_for_code()
        # root_key, 
        # key_type,# 契合 root_key, 我们这里就不 parse append_key
        return param
    def out_fields(self, prev_fields):
        root_key = []
        key_type = 'str'
        return [*self.table.out_fields(prev_fields), 
            root_key, key_type, 
        ]


