class Panda_functor:
    def ReadMysqlDb(self, 
        db_name, tb_name, tb_cn_name, 
        base_field_list, base_comment_list, 
        select_list, base_cond_list,
    ):
        # base_data = self.functor.base_data
        # # param = self.functor.code_param
        # # 'table_info': {'table_schema': 'db_aliyun', 'table_name': 'sy_cd_ms_sh_gs_shlist_new', 'table_comment': '工商股东表', 'table_catalog': 'def', 'table_rows': 0, 'avg_row_length': 0}
        # print('base_data', base_data)
        # db_name = base_data['table_info']['table_schema']
        # tb_name = base_data['table_info']['table_name']
        # tb_cn_name = base_data['table_info']['table_comment']
        
        # base_field_list = base_data['field_list'][1:]
        # base_comment_list = base_data['comment_list'][1:]
        # select_list = base_data['select_list'][1:]
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
            # for cond in base_data['cond_list']
            for cond in base_cond_list
            if cond.strip() != ''
        ])
        # print('readMysql:parse', param)
        r = f"""
def f_root():
    "ReadMysqlDb"
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
        cond_list = ' AND '.join([
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
    
    def SaveExcel(self, 
        excel_name, rename_dict
    ):
        select_list = rename_dict.keys()
        rename_list = rename_dict.values()
        def field_to_code(field_list):
            field_list = [
                f"'{field}',"
                for field in field_list
            ]
            return """
                """.join(field_list)
        
        r = f"""
def f_save(df):
    "SaveExcel"
    print('save.df', df)
    with pandas.ExcelWriter("{excel_name}.xlsx") as writer:
        df = df[[
            {field_to_code(select_list)}
        ]]
        df = df.set_axis(
        [
            {field_to_code(rename_list)}
        ], axis=1)
        df.to_excel(writer, sheet_name="{excel_name}", index=False)
            """.strip()
        return r


panda_functor = Panda_functor()