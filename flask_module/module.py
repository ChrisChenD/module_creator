#!/usr/bin/env python3
from flask_module.utils.mysql_utils import ReadMysql

class Module:
    def __init__(self, db_name, table_name) -> None:
        self.db_name = db_name
        self.table_name = table_name
    @property
    def field_list(db_name, table_name):
        field_list = []
        try:
            rows = ReadMysql(f"test:test@127.0.0.1:3306/{db_name}")(
                f"SHOW FULL COLUMNS FROM {table_name}")
            cols = "Field,Type,Collation,Null,Key,Default,Extra,Privileges,Comment".split(',')
            field_list = [
                dict(zip(cols, row)) for row in rows
            ]
            # print('info_list', info_list)
            # table comment
            # comment,catalog,rows_num,avg_rowlen
        except:
            import traceback;print(traceback.format_exc())
        return field_list

    @property
    def table_info(db_name, table_name):
        table_info = []
        try:
            rows = ReadMysql(f"test:test@127.0.0.1:3306/{db_name}")(
                f"""SELECT TABLE_SCHEMA,TABLE_NAME,TABLE_COMMENT,TABLE_CATALOG,TABLE_ROWS,AVG_ROW_LENGTH
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_SCHEMA='{db_name}' and table_name='{table_name}';"""
            )
            cols = 'table_schema,table_name,table_comment,table_catalog,table_rows,avg_row_length'.split(',')
            table_info = [dict(zip(cols, row)) for row in rows][0]
            # print('db_name,table_name,TABLE_COMMENT,TABLE_CATALOG,TABLE_ROWS,AVG_ROW_LENGTH', comment,catalog,rows_num,avg_rowlen)
            # print('r', r)
            # module_info['info'] = {
            #     'field_list':field_list,
            #     'table_info':table_info
            # }
            # WHERE TABLE_SCHEMA='db152' and table_name='sy_cd_ms_base_gs_comp_info_new';
        except:
            import traceback;print(traceback.format_exc())
        return table_info
# rows = ReadMysql(f"test:test@127.0.0.1:3306/{db_name}")(
#     f"SHOW FULL COLUMNS FROM {table_name}")
# cols = "Field,Type,Collation,Null,Key,Default,Extra,Privileges,Comment".split(',')
# field_list = [dict(zip(cols, row)) for row in rows]
# # print('info_list', info_list)
# # table comment
# # comment,catalog,rows_num,avg_rowlen


# class Table:
#     def __init__(self, name, name_ext, fields):
#         self.name = name
#         self.name_ext = name_ext
#         self.fields = fields
#         # this.name = data.name//string
#         # this.name_ext = data.name_ext
#         # this.fields = data.fields
    



