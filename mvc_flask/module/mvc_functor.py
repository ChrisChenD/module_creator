#!/usr/bin/env python3
import copy
from module.module_base import Module_base, Module_root, module_info
# 普通的类/叶子节点继承 Module_base
# 作为模型根节点 继承 Module_root
from module.compo import Com, Module_base_debug
from mvc_flask.module.mysql_lib.mysql_module import Mysql_module
# debug的叶子节点, 继承 Module_base_debug
# 这个效果是自动给类分配一个内容(类的名字), 用来观察

cls1 = 'bg-stone-700 border-4 text-white'


@module_info.registry
class ReadMysqlDb_Table(Module_base):
    @staticmethod
    def m(): 
        return dict(
        db_chain=Com.Com_P,
        db_chain_note=Com.Com_P,
        com_table=Com.Com_Table,
    )
    
    def init(self, db_chain):
        self.db_chain_note.init(f'note:[{db_chain}]')

    def load_module(self, text):
        db_chain = text
        self.db_chain.init(db_chain)
        self.mysql_module = Mysql_module()
        print(f"load_module: text[{db_chain}]")
        self.mysql_module.get_module(db_chain)
        
        self.select_list = [True]*len(self.mysql_module.field_list)
        self.cond_list = ['']*len(self.mysql_module.field_list)
        self.field_list = [field['Field'] for field in self.mysql_module.field_list]
        self.comment_list = [field['Comment'] for field in self.mysql_module.field_list]
        self.type_list = [field['Type'] for field in self.mysql_module.field_list]
        self.table_info = self.mysql_module.table_info
        self.build_table()

    def build_table(self):
        name_list=[
            Com.Com_P(self.com_table, field)
            for field in ['Field']+self.field_list
        ]
        comment_list=[
            Com.Com_P(self.com_table, field)
            for field in ['Comment']+self.comment_list
        ]
        type_list=[
            Com.Com_P(self.com_table, field)
            for field in ['Type']+self.type_list
        ]
        select_list = [
            Com.Com_Button(self.com_table, 
                value="[X]" if is_selected else '_._',
                onClick=[
                    self.idx,
                    'select',
                    dict(idx=idx-1)
                ],
            )
            for idx, is_selected in enumerate([True]+self.select_list)
        ]
        cond_list = [
            Com.Com_text(self.com_table,
                text=cond,
                onEnter=[
                    self.idx,
                    'set_cond',
                    dict(idx=idx-1)
                ]
            )
            for idx,cond in enumerate(['cond']+self.cond_list)
        ]
        self.com_table.init(e_list=[
            name_list,
            comment_list,
            type_list,
            select_list,
            cond_list
        ])
        print('self.cond_list', self.cond_list)
    def select(self, idx):
        self.select_list[idx] = not self.select_list[idx]
        self.build_table()
    def set_cond(self, idx, text):
        print(f'set_cond(idx={idx}, text="{text}")')
        self.cond_list[idx] = text
        self.build_table()
    def out_fields(self):
        fields = []
        for i,field in enumerate(self.field_list):
            if self.select_list[i] is True:
                fields.append(field)
        return fields
    def param_for_code(self):
        table_info = self.table_info
        # table_schema,table_name,table_comment,table_catalog,table_rows,avg_row_length
        db_name = table_info['table_schema']
        tb_name = table_info['table_name']
        tb_cn_name = table_info['table_comment']
        base_field_list = self.field_list
        base_comment_list = self.comment_list
        select_list = self.select_list
        base_cond_list = self.cond_list
        return (
            db_name, tb_name, tb_cn_name, 
            base_field_list, base_comment_list, 
            select_list, base_cond_list,
        )
        # self.select_list = [True]*len(self.mysql_module.field_list)
        # self.cond_list = ['']*len(self.mysql_module.field_list)
        # self.field_list = [field['Field'] for field in self.mysql_module.field_list]
        # self.comment_list = [field['Comment'] for field in self.mysql_module.field_list]
        # self.type_list = [field['Type'] for field in self.mysql_module.field_list]

        # pass


@module_info.registry
class Table2(ReadMysqlDb_Table):
    @staticmethod
    def m(): 
        return dict(
        db_chain=Com.Com_P,
        db_chain_note=Com.Com_P,
        com_table=Com.Com_Table,
    )
    def load_module(self, text):
        db_chain = text
        self.db_chain.init(db_chain)
        self.mysql_module = Mysql_module()
        print(f"load_module: text[{db_chain}]")
        self.mysql_module.get_module(db_chain)
        
        self.select_list = [True]*len(self.mysql_module.field_list)
        self.cond_list = ['']*len(self.mysql_module.field_list)
        self.key_list = []
        self.prev_field_list = ['prev_field1', 'prev_field2']
        self.build_table()
    def build_table(self):
        name_list=[
            Com.Com_P(self.com_table, field)
            for field in ['Field']+[field['Field'] for field in self.mysql_module.field_list]
        ]
        comment_list=[
            Com.Com_P(self.com_table, field)
            for field in ['Comment']+[field['Comment'] for field in self.mysql_module.field_list]
        ]
        type_list=[
            Com.Com_P(self.com_table, field)
            for field in ['Type']+[field['Type'] for field in self.mysql_module.field_list]
        ]
        select_list = [
            Com.Com_Button(self.com_table, 
                value="[X]" if is_selected else '_._',
                onClick=[
                    self.idx,
                    'select',
                    dict(idx=idx-1)
                ],
            )
            for idx, is_selected in enumerate([True]+self.select_list)
        ]
        cond_list = [
            Com.Com_text(self.com_table,
                text=cond,
                onEnter=[
                    self.idx,
                    'set_cond',
                    dict(idx=idx-1)
                ]
            )
            for idx,cond in enumerate(['cond']+self.cond_list)
        ]
        key_list=[
            Com.Com_P(self.com_table, field)
            for field in ['Key']+[field['Key'] for field in self.mysql_module.field_list]
        ]
        self.com_table.init(e_list=[
            name_list,
            comment_list,
            type_list,
            select_list,
            cond_list,
            key_list
        ])
        print('self.cond_list', self.cond_list)

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
            table=Table2
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
        


