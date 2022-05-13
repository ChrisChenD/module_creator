#!/usr/bin/env python3

class Panda_code:
    def __init__(self, functor, functor_id) -> None:
        self.functor = functor
        self.functor_id = functor_id
    @staticmethod
    def import_libs():
        return f"""
from pandaUtil_mysql_chain import mysql_chain
from pandaUtil_append import chunk_append,readMysql
        """.strip()

    @property
    def code(self):
        method = self.functor.__class__.__name__
        return getattr(self, method)()

    def readMysql(self):
        base_data = self.functor.base_data
        # param = self.functor.code_param
        # 'table_info': {'table_schema': 'db_aliyun', 'table_name': 'sy_cd_ms_sh_gs_shlist_new', 'table_comment': '工商股东表', 'table_catalog': 'def', 'table_rows': 0, 'avg_row_length': 0}
        print('base_data', base_data)
        db_name = base_data['table_info']['table_schema']
        tb_name = base_data['table_info']['table_name']
        tb_cn_name = base_data['table_info']['table_comment']
        
        base_field_list = base_data['field_list'][1:]
        base_comment_list = base_data['comment_list'][1:]
        select_list = base_data['select_list'][1:]
        select_field_list = ",".join([
            field
            for i,field in enumerate(base_field_list)
            if select_list[i]==True
        ])
        select_comment_list = ','.join([
            commend
            for i,commend in enumerate(base_comment_list)
            if select_list[i]==True
            
        ])
        cond_list = ','.join([
            cond
            for cond in base_data['cond_list']
            if cond.strip() != ''
        ])
        # print('readMysql:parse', param)
        r = f"""
def f_root():
    "{self.functor.__class__.__name__}"
    # {tb_cn_name}
    # {select_comment_list}
    for chunk in readMysql(mysql_chain.{db_name})[
        "{tb_name}",
        "{select_field_list}",
        "{cond_list}",
    ].df_chunks:
        yield chunk
        """.strip()
        return r
    
    def colAppend(self):
        base_data = self.functor.base_data
        print('base_data', base_data)
        db_name = base_data['table_info']['table_schema']
        tb_name = base_data['table_info']['table_name']
        tb_cn_name = base_data['table_info']['table_comment']
        
        base_field_list = base_data['field_list'][1:]
        base_comment_list = base_data['comment_list'][1:]
        select_list = base_data['select_list'][1:]
        key_list = base_data['key_list'][1:]
        select_field_list = ",".join([
            field
            for i,field in enumerate(base_field_list)
            if select_list[i]==True
        ])
        select_comment_list = ','.join([
            commend
            for i,commend in enumerate(base_comment_list)
            if select_list[i]==True
            
        ])
        cond_list = ','.join([
            cond
            for cond in base_data['cond_list']
            if cond.strip() != ''
        ])
        # def chunk_append(root_chunk, append_info, key, key_type=str):
        key_type = 'str'
        # append_key_list = [
        #     field
        #     for i,field in enumerate(base_field_list)
        #     if key_list[i]==True
        # ]
        # append_key = ''
        # if len(append_key_list)>0:
        #     append_key = append_key_list[0]
        append_key = base_data.get('append_key', '')
        root_key = base_data.get('prev_root_key', '')

        r = f"""
def f{self.functor_id}(chunk):
    "{self.functor.__class__.__name__}"
    # {tb_cn_name}
    # {select_comment_list}
    root_key,append_key = {root_key},{append_key}
    new_chunk = chunk_append(chunk, append_info=[
        mysql_chain.{db_name},
        "{tb_name}",
        "{select_field_list}",
        "{cond_list}",
    ], key=[
        root_key,append_key
    ], key_type={key_type})
    return new_chunk
        """.strip()
        return r
    
    def saveExcel(self):
        r = f"""
def f_save(df):
    "{self.functor.__class__.__name__}"
    print('save.df', df)
        """.strip()
        return r



