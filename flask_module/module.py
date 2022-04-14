#!/usr/bin/env python3
from operator import truediv
from flask_module.utils.mysql_utils import ReadMysql
import copy

class Functor:
    def __init__(self) -> None:
        self.base_data = dict(
            name=self.__class__.__name__
        )
    @property
    def data(self):
        data = copy.deepcopy(self.base_data)
        return data
    @property
    def json_base(self):
        return self.data
    def op(self, **data):
        func = data['method']
        func = func[len('functor_'):]
        import copy
        params = copy.deepcopy(data)
        del params['method']
        del params['functor_id']
        getattr(self, func)(**params)
        return None
class MysqlFunctor(Functor):
    def default_cond_list(self):
        field_list = self.base_data['field_list']
        cond_list = copy.deepcopy(self.base_data['cond_list'])
        for i in range(len(field_list)):
            field = field_list[i]
            if field == 'dataStatus':
                cond_list[i] = 'dataStatus!=3'
            if field == 'isValid':
                cond_list[i] = 'isValid=1'
        return cond_list
        
    def default_select_list(self):
        select_list = [True]*len(self.base_data['field_list'])
        for i,field in enumerate(self.base_data['field_list']):
            if field in 'id,dataStatus,modifyTime,createTime'.split(','):
                print('field!', field)
                select_list[i] = False
        return select_list
    
    def map_id(self, field_id):
        # 因为我们重排了列的位置，(true在前)需要逻辑映射
        select_list = self.base_data['select_list']
        id_map = [
            i
            for i,b in enumerate(select_list) if b==True
        ]+[
            i
            for i,b in enumerate(select_list) if b==False
        ]
        return id_map[field_id]

    def select_switch(self, field_id):
        if field_id == 0:
            if self.base_data['select_list'][0] == False:
                # 全不选->默认
                self.base_data['select_list'] = self.default_select_list()
                self.base_data['select_list'][0] = True
            else:
                # 默认->全不选
                self.base_data['select_list'] = [False]*len(self.base_data['select_list'])
                self.base_data['select_list'][0] = False
        else:
            field_id = self.map_id(field_id)
            self.base_data['select_list'][field_id] = not self.base_data['select_list'][field_id]

    def modify_cond(self, field_id, cond):
        field_id = self.map_id(field_id)
        self.base_data["cond_list"][field_id] = cond


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
    


class readMysql(MysqlFunctor):
    def load_chain(self, db_chain) -> None:
        self.db_name, self.table_name = db_chain.split(".")
        self.base_data = {
            'name':self.__class__.__name__,
            'table_info':self.table_info,
            'field_list':['field_list']+[field['Field'] for field in self.field_list],
            'comment_list':['comment_list']+[field['Comment'] for field in self.field_list],
            'cond_list':['cond_list']+['']*len(self.field_list),
            'select_list':[True]+[True]*len(self.field_list),
        }
        self.base_data['select_list'] = self.default_select_list()
        self.base_data['cond_list'] = self.default_cond_list()
    @property
    def data(self):
        data = copy.deepcopy(self.base_data)
        if 'select_list' not in data:
            return data
        select_list = self.base_data['select_list']
        
        for col_list in 'field_list,comment_list,cond_list,select_list'.split(','):
            data[col_list] = [{
                'value':data[col_list][0],
                'selected':True
            }]+[{
                'selected':select_list[i],
                'value':value,
            } for i,value in enumerate(self.base_data[col_list])
                if select_list[i] == True and i>0
            ]+[{
                'selected':select_list[i],
                'value':value,
            } for i,value in enumerate(self.base_data[col_list])
                if select_list[i] == False and i>0
            ]
        data["select_list"][0]['value'] = '默认' if select_list[0] else '全不选'
        return data
class saveExcel(Functor):
    pass

class colAppend(MysqlFunctor):
    ""
    def load_chain(self, db_chain) -> None:
        self.db_name, self.table_name = db_chain.split(".")
        self.base_data = {
            'name':self.__class__.__name__,
            'table_info':self.table_info,
            'field_list':['field_list']+[field['Field'] for field in self.field_list],
            'comment_list':['comment_list']+[field['Comment'] for field in self.field_list],
            'cond_list':['cond_list']+['']*len(self.field_list),
            'select_list':[True]+[True]*len(self.field_list),
            'key_list':[
                dict(value='key_list', selected=False) 
                ]+[
                dict(value=field['Key'], selected=False) 
                for field in self.field_list
            ],
        }
        self.base_data['select_list'] = self.default_select_list()
        self.base_data['cond_list'] = self.default_cond_list()
    def select_key(self, field_id):
        field_id = self.map_id(field_id)
        self.base_data['key_list'][field_id]['selected'] = not self.base_data['key_list'][field_id]['selected']
        
    
    @property
    def data(self):
        data = copy.deepcopy(self.base_data)
        if 'select_list' not in data:
            return data
        select_list = self.base_data['select_list']
        
        for col_list in 'field_list,comment_list,cond_list,select_list,key_list'.split(','):
            data[col_list] = [{
                'value':data[col_list][0],
                'selected':True
            }]+[{
                'selected':select_list[i],
                'value':value,
            } for i,value in enumerate(self.base_data[col_list])
                if select_list[i] == True and i>0
            ]+[{
                'selected':select_list[i],
                'value':value,
            } for i,value in enumerate(self.base_data[col_list])
                if select_list[i] == False and i>0
            ]
        data["select_list"][0]['value'] = '默认' if select_list[0] else '全不选'
        return data

    
