#!/usr/bin/env python3
import copy
from module.module_base import Module_base, Module_root, module_info
# 普通的类/叶子节点继承 Module_base
# 作为模型根节点 继承 Module_root
# from module.compo import Com, Module_base_debug
from module.compo_canvas import Com_canvas as Com
from plan_flask.module.mysql_lib.mysql_module import Mysql_module

cls_default = 'bg-stone-700 border-4 text-white'
cls_sky = 'bg-sky-200 border-4 text-black'
cls_select = lambda selected: cls_sky if selected else cls_default


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

    def cls_name_gen(self, idx):
        return cls_select(([True]+self.select_list)[idx])

    def build_table(self):
        # cls_name_gen = lambda idx: cls_select(([True]+self.select_list)[idx])
        name_list=[
            Com.Com_P(self.com_table, field,
                cls_name=self.cls_name_gen(idx)
            )
            for idx, field in enumerate(['Field']+self.field_list)
        ]
        comment_list=[
            Com.Com_P(self.com_table, field,
                cls_name=self.cls_name_gen(idx)
            )
            for idx, field in enumerate(['Comment']+self.comment_list)
        ]
        type_list=[
            Com.Com_P(self.com_table, field,
                cls_name=self.cls_name_gen(idx)
            )
            for idx, field in enumerate(['Type']+self.type_list)
        ]
        select_list = [
            Com.Com_Button(self.com_table, 
                value="[X]" if is_selected else '..',
                onClick=[
                    self.idx,
                    'select',
                    dict(idx=idx-1)
                ],
                cls_name=self.cls_name_gen(idx)
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
                ],
                cls_name=self.cls_name_gen(idx)
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


@module_info.registry
class Table2(ReadMysqlDb_Table):
    @staticmethod
    def m(): 
        return dict(
            db_chain=Com.Com_P,
            db_chain_note=Com.Com_P,
            com_table=Com.Com_Table,
            # prev_fields_select=Com.Com_Line,
        )
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
        self.key_list = []
        self.key_idx = 0
        self.build_table()

    
    def select_key(self, key_idx):
        self.key_idx = key_idx
        print('select_key:', key_idx)
        self.build_table()
    

    def append_key(self): return self.key_list[self.key_idx]
    def cls_name_gen_key(self, idx):
        return cls_select(self.key_idx == idx-1)


    def build_table(self):
        name_list=[
            Com.Com_P(self.com_table, field,
                cls_name=self.cls_name_gen(idx)
            )
            for idx, field in enumerate(['Field']+self.field_list)
        ]
        comment_list=[
            Com.Com_P(self.com_table, field,
                cls_name=self.cls_name_gen(idx)
            )
            for idx, field in enumerate(['Comment']+self.comment_list)
        ]
        type_list=[
            Com.Com_P(self.com_table, field,
                cls_name=self.cls_name_gen(idx)
            )
            for idx, field in enumerate(['Type']+self.type_list)
        ]
        select_list = [
            Com.Com_Button(self.com_table, 
                value="[X]" if is_selected else '..',
                onClick=[
                    self.idx,
                    'select',
                    dict(idx=idx-1)
                ],
                cls_name=self.cls_name_gen(idx)
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
                ],
                cls_name=self.cls_name_gen(idx)
            )
            for idx,cond in enumerate(['cond']+self.cond_list)
        ]
        # self.com_table.init(e_list=[
        #     name_list,
        #     comment_list,
        #     type_list,
        #     select_list,
        #     cond_list
        # ])
        key_list=[
            # Com.Com_P(self.com_table, field)
            Com.Com_Button(self.com_table, 
                value=field if field else '__',
                onClick=[
                    self.idx,
                    'select_key',
                    dict(key_idx=idx-1)
                ],
                cls_name=self.cls_name_gen_key(idx)
            )
            for idx,field in enumerate(['Key']+self.field_list)
        ]
        
        self.com_table.init(e_list=[
            name_list,
            comment_list,
            type_list,
            select_list,
            cond_list,
            key_list
        ])
        # self.prev_fields_select.init(e_list=[
        #     Com.Com_Line(self, e_list=[
        #         # Com.Com_P(self, value=field),
        #         # Com.Com_text(self, text=self.rename_list[idx],
        #     Com.Com_Button(self.com_table, 
        #         value=field if field else '__',
        #             onClick=[
        #                 self.idx,
        #                 'select_prev_key',
        #                 dict(key_idx=idx-1)
        #             ]
        #         )
        #     ])
        #     for idx,field in enumerate(self.prev_field_list)
        # ])
        # print('self.cond_list', self.cond_list)
        
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
        append_key = self.append_key()
        # root_key = self.prev_key()
        # key_type = 'str'
        return (
            # db_name, tb_name, tb_cn_name, 
            # base_field_list, base_comment_list, 
            # select_list, base_cond_list,
            db_name, tb_name, tb_cn_name, 
            base_field_list, base_comment_list, 
            select_list, base_cond_list,
            append_key
            # root_key, key_type, 
            # 
        )
    # def x(self):        
    #     self.key_list = []
    #     self.key_idx = 0
    #     self.prev_field_list = ['prev_field1', 'prev_field2']
    #     self.prev_key_idx = 0
    