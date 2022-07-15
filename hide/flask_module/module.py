#!/usr/bin/env python3
from operator import truediv
from flask_module.utils.mysql_utils import ReadMysql
import copy
from flask_module.module_lines import Item_line, Field_line,Comment_line,Cond_line,Select_line,Key_line,Prev_line

class Functor:
    def __init__(self) -> None:
        self.base_data = dict(
            name=self.__class__.__name__
        )
    @property
    def json_base(self):
        data = copy.deepcopy(self.base_data)
        return data
        # return self.data
    def op(self, **data):
        func = data['method']
        func = func[len('functor_'):]
        import copy
        params = copy.deepcopy(data)
        del params['method']
        del params['functor_id']
        getattr(self, func)(**params)
        return None

    # current_fields,prev_fields
    @property
    def not_load(self):
        return 'prev_list' not in self.base_data
    @property
    def current_fields(self):
        if self.not_load: return []
        fields = copy.deepcopy(self.base_data['prev_list'].prev_list)
        fields.extend(self._selected_field_list())
        return fields
    def set_prev_fields(self, prev_fields):
        if self.not_load: return
        self.base_data['prev_list'].prev_list = copy.deepcopy(prev_fields)
        #  = 
    def _selected_field_list(self):
        field_list = []
        select_list = self.base_data.get('select_list', None)
        if select_list is not None:
            field_list = [
                field
                for i,field in enumerate(self.base_data['field_list'].data_list)
                if self.base_data['select_list'].data_list[i] is True
            ]
        print('_selected_field_list')
        print('select_list', select_list)
        print('field_list', field_list)
        return field_list


class MysqlFunctor(Functor):

    def select_switch(self, field_id):
        self.base_data['select_list'].select_switch(field_id)

    def modify_cond(self, field_id, cond):
        cond_line = self.base_data['cond_list']
        cond_line.set(cond_line._real_id(field_id), cond)


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
    
    def item_list(self):
        return list(self.item_map().keys())
    def item_map(self):
        from module_lines import item_map
        return item_map(self.field_list)

    def init_base_data(self):
        self.base_data = {
            'name':self.__class__.__name__,
            'table_info':self.table_info,
        }
        for item,item_value in self.item_map().items():
            # print('{self.__class__.__name__}.init_base_data:', item)
            self.base_data[item] = item_value

    @property
    def json_base(self):
        data = copy.deepcopy(self.base_data)
        if 'select_list' not in data:
            return data
        for col_list in self.item_list():
            data[col_list] = self.base_data[col_list].selected_data()
        return data

class readMysql(MysqlFunctor):
    def load_chain(self, db_chain) -> None:
        self.db_name, self.table_name = db_chain.split(".")
        self.init_base_data()
    
class saveExcel(Functor):
    def load_chain(self, db_chain) -> None:
        self.base_data['db_chain'] = db_chain
    
    @property
    def json_base(self):
        return self.base_data

class colAppend(MysqlFunctor):
    ""
    def item_map(self):
        from module_lines import item_map2
        return item_map2(self.field_list)

    def load_chain(self, db_chain) -> None:
        self.db_name, self.table_name = db_chain.split(".")
        self.init_base_data()

    # def select_key(self, field_id):
    #     field_id = self._map_id(field_id)
    #     self.base_data['key_list'][field_id]['selected'] = not self.base_data['key_list'][field_id]['selected']
    def select_chunk_key(self, field_id):
        self.base_data['prev_list'].select_chunk_key(field_id)
    
    def set_append_key(self, field_id):
        self.base_data['append_key'] = self.base_data['select_list'][field_id]
    def set_root_key(self, prev_id):
        self.base_data['prev_root_key'] = self.base_data['prev_fields'][prev_id]

