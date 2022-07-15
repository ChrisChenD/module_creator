
from plan_flask.module.mysql_lib.ReadMysql import ReadMysql

class Mysql_module:
    field_cols = 'Field,Type,Collation,Null,Key,Default,Extra,Privileges,Comment'.split(',')
    info_cols = 'table_schema,table_name,table_comment,table_catalog,table_rows,avg_row_length'.split(',')
    def __init__(self, db_chain=''):
        self.db_chain = db_chain
        self.field_list = []
        self.table_info = dict()
    # @classmethod
    def get_module(self, db_chain):

        db_name, table_name = db_chain.split('.')
        # module_info = dict(
        #    db_table_name = db_chain,
        #    info = None
        # )
        try:
            db_string = f"test:test@localhost:3306/{db_name}"
            sql = f"SHOW FULL COLUMNS FROM {table_name}"
            print('db_string', db_string)
            print('sql', sql)

            rows = ReadMysql(db_string)(sql)
                
            # cols = "Field,Type,Collation,Null,Key,Default,Extra,Privileges,Comment".split(',')
            self.field_list = [dict(zip(self.field_cols, row)) for row in rows]
            rows = ReadMysql(f"test:test@127.0.0.1:3306/{db_name}")(
                f"""SELECT TABLE_SCHEMA,TABLE_NAME,TABLE_COMMENT,TABLE_CATALOG,TABLE_ROWS,AVG_ROW_LENGTH
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA='{db_name}' and table_name='{table_name}';""")
            # cols = 'table_schema,table_name,table_comment,table_catalog,table_rows,avg_row_length'.split(',')
            self.table_info = [dict(zip(self.info_cols, row)) for row in rows]
            self.table_info = self.table_info[0]
            # module_info['info'] = {
            #     'field_list':field_list,
            #     'table_info':table_info
            # }
        except:
            import traceback;print(traceback.format_exc())
            raise Exception('get_module Error!')
        return self


mysql_module = Mysql_module()