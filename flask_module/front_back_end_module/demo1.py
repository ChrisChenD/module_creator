#!/usr/bin/env python3
import pandas, numpy
from db_utils.ReadMysql3 import ReadMysql3
import db_utils.mysql_string as mysql_string
import config.common_var as common_var  
from db_utils.Excel import Excel
# from module_common import Column
from big_file.mysql_pymodule import mysql
from module import module
import copy
pandas.set_option('max_columns', None)

class Db:
    def db152(): return ReadMysql3(mysql_string.db152)
    def db136_sydb(): return ReadMysql3(mysql_string.db136_sydb)
    def db136_dbsy(): return ReadMysql3(mysql_string.db136_dbsy)
    def db_aliyun(): return ReadMysql3(mysql_string.db_aliyun)

class Module:
    def __init__(self, **kwargs):
        self.kwargs = dict(**copy.deepcopy(kwargs))
    def __call__(self, **kwargs):
        'modify inplace'
        self.kwargs.update(copy.deepcopy(kwargs))
        return self
    def copy(self, **kwargs):
        'clone'
        # return copy.deepcopy(self)(**kwargs)
        new_module = self.__class__(**self.kwargs)
        return new_module(**kwargs)
    def get(self, key, default_value=None):
        return self.kwargs.get(key, default_value)
    def setitem(self, key, value):
        self.kwargs[key] = value

    # @staticmethod
    # def table(db_name):

class Table(Module):
    db_name = ''
    def __init__(self, **kwargs):
        "chunk,chunkn,select,cond,sql_on"
        super().__init__(**kwargs)
        # self.db_name = db_name
        self.engine = getattr(Db, self.db_name)()
    # @staticmethod
    @property
    def table_name(self): return self.__class__.__name__

    class List_engine:
        def __init__(self, cond_list, gap=','):
            if not isinstance(cond_list, list): cond_list = [cond_list]
            self.cond_list = cond_list
            self.gap = gap
        def __add__(self, cond_list):
            if not isinstance(cond_list, list): cond_list = [cond_list]
            return self.__class__([
                *self.cond_list, *cond_list
            ])
        def __str__(self): 
            return self.gap.join(self.cond_list)
    class Cond_engine(List_engine):
        def __init__(self, cond_list): super().__init__(cond_list, gap=' AND ')
    @property
    def cond(self):
        r = self.get('cond', ["1"])
        return r if isinstance(r, self.Cond_engine) else self.Cond_engine(r)
    @cond.setter
    def cond(self, v):
        self.setitem('cond', 
            self.Cond_engine(v) if not isinstance(v, self.Cond_engine) else v
        )
    @property
    def fields(self):
        r = self.get('fields', ["*"])
        return r if isinstance(r, self.List_engine) else self.List_engine(r)
    @fields.setter
    def fields(self, v):
        self.setitem('fields', 
            self.List_engine(v) if not isinstance(v, self.List_engine) else v
        )

    @property
    def df_chunks(self):
        chunksize = self.get('chunk', 50)
        chunknum = self.get('chunkn', -1)
        tname = self.table_name
        # select = self.get('select', '*')
        fields = str(self.fields)
        cond = str(self.cond)
        printsql = self.get('sql_on', False)
        full_data = self.get('full_data', False)

        dfs = self.engine.print_sql(
            printsql
        ).full_data(full_data).set_chunk(
            chunksize = chunksize,
            chunknum = chunknum
        )[
            tname,
            fields, 
            cond
        ].df_chunks
        for i,df in enumerate(dfs):
            print(f'table: {self.table_name}| {df.columns}')
            yield df
    @property
    def df(self):
        dfs = [df for df in self.df_chunks]# iter to list
        df = pandas.concat(dfs, axis=0)
        # df.reset_index(inplace=True)
        return df
    #### 
    def append_fields_by_keys(self, df, df_key, fields):
        print('table_name', self.table_name)
        return self.append(df, 
            {self.get('key'):df_key}, 
            fields)
    def append(self, df, key_map, fields):
        self_key, df_key = None, None
        for k,v in key_map.items():
            self_key,df_key = k,v
        return self.copy(select=fields+[self_key,]).merge(df, [df_key, [self_key, df_key]])
    
    # def append_df(self, df, df_key, self_key):
    #     ext_df = self.merge(df, [df_key, [self_key, df_key]])
    #     new_df = self._chunk_reorder(df, ext_df, [df_key]*2)
    #     return new_df
    def merge(self, chunk, key, _type=str):
        'key:  [on_key, [l_key, r_key]]'
        '与一个 df_chunk merge '
        table = self.copy()
        on_key, (table_key, chunk_key) = key
        # c = table.copy()
        "join values"
        name_list = chunk.loc[:,chunk_key]
        name_tuple = list(filter(None,set(name_list)))
        name_tuple_str = str(tuple(_type(name) for name in name_tuple))
        if len(name_tuple) == 1:
            name_tuple_str = f"({name_tuple_str[1:-2]})"# [:-2]+name_tuple_str[-1:]

        'cond culculate'
        # table.kwargs['cond'] += f' and {table_key} in {name_tuple_str}'
        table.cond = table.cond + f'{table_key} in {name_tuple_str}'
        if len(name_tuple) == 0:
            table.cond = "0"
        'query'
        df = table.df
        # print('table.feilds', table.fields)
        # print('df.columns', df.columns)
        # print('chunk.columns', chunk.columns)
        
        "name coordinate"
        if on_key != table_key:
            df.rename(columns={table_key:on_key}, inplace=True)
        if on_key != chunk_key:
            chunk.rename(columns={chunk_key:on_key}, inplace=True)
        # row_debug = [None]
        try:
            chunk = pandas.merge(df, chunk, on=on_key, suffixes=['',''], how='inner')
        except:
            import traceback;print(traceback.format_exc())
            print("df.columns", df.columns)
            print("chunk.columns", chunk.columns)
            print('key:', on_key)
            print('common key:', set(df.columns)&set(chunk.columns))
            # print('row debug', row_debug[0])
            exit()
        return chunk
        # return Table

class module:
    class db136_sydb:
        class dwd_ms_cn_px_list(Table):db_name = "db136_sydb"
        class dwd_ms_cn_px_pdt_info(Table):db_name = "db136_sydb"
        class dwd_ms_cn_px_invo_info(Table):db_name = "db136_sydb"
    class db136_dbsy:
        class dwd_mm_cn_smjj_info(Table):db_name = "db136_dbsy"
        class dwd_mm_cn_smjj_wba_info(Table):db_name = "db136_dbsy"
    class db_aliyun:
        class sy_cd_ms_base_gs_comp_info_new(Table):db_name = "db_aliyun"
        class sy_cd_ms_sh_gs_shlist_new(Table):db_name = "db_aliyun"


px_list = module.db136_sydb.dwd_ms_cn_px_list(
    fields = "spectrumId,spectrumName,nameType".split(','),
    cond='dataStatus!=3'
)
px_pdt_info = module.db136_sydb.dwd_ms_cn_px_pdt_info(
    fields = "spectrumId,cName,category,registerCapital,legalRepresent,establishDate,regStatus".split(','),
    cond='dataStatus!=3'
)
px_invo_info = module.db136_sydb.dwd_ms_cn_px_invo_info(
    fields = "spectrumId,cName,category,registerCapital,legalRepresent,establishDate,regStatus".split(','),
    cond='dataStatus!=3'
) 

smjj_info = module.db136_dbsy.dwd_mm_cn_smjj_info(
    fields = "fundName,operateStatus,productId,registerDate,subType,trusteeName,manageName".split(','),
    cond='dataStatus!=3'
)
smjj_wba_info = module.db136_dbsy.dwd_mm_cn_smjj_wba_info(
    fields = "fundCode,fundName,creditCode,estiblishDate,manageCode,manageName,property1,property2,property3,property4".split(','),
    cond='dataStatus!=3'
)

gs_comp_info = module.db_aliyun.sy_cd_ms_base_gs_comp_info_new(
    fields = "compName,compCode,stateAbbr,legalPersonId,legalPersonName".split(','),
    cond='dataStatus!=3'
)

gs_shlist = module.db_aliyun.sy_cd_ms_sh_gs_shlist_new(
    fields = "compCode,shId,shTypeCode,shName,holdRatio".split(','),
    cond='dataStatus!=3'
)

name_map = dict()
df_list = []
# 1、导出 谱系下机构信息 dwd_ms_cn_px_invo_info 数据,并关联出其他字段
# for df in px_invo_info(chunk=10).df_chunks:
for i,chunk in enumerate(px_invo_info(chunk=50).df_chunks):
    print('i', i)
    # 谱系名称    dwd_ms_cn_px_list.spectrumName   通过 spectrumId 关联，并筛选 nameType=1
    df = px_list.copy(key='spectrumId', cond=px_list.cond+'nameType=1'
        ).append_fields_by_keys(chunk, 'spectrumId', ['spectrumName'])
    name_map['spectrumName'] = '谱系名称'
    # 机构名称    dwd_ms_cn_px_invo_info.cName
    name_map['cName'] = '机构名称'
    # 机构类型    dwd_ms_cn_px_invo_info.category
    name_map['category'] = '机构类型'
    # 省份简称    sy_cd_ms_base_gs_comp_info_new.stateAbbr  通过 cName 与 compName 关联
    # 法人ID      sy_cd_ms_base_gs_comp_info_new.legalPersonId  通过 cName 与 compName 关联
    # 法人姓名    sy_cd_ms_base_gs_comp_info_new.legalPersonName  通过 cName 与 compName 关联
    # 通过 cName 先与 sy_cd_ms_base_gs_comp_info_new 关联，查询 compCode

    df = gs_comp_info.copy(key='compName',full_data=True
        ).append_fields_by_keys(df, 'cName', 
            ['stateAbbr','legalPersonId','legalPersonName','compCode'])
    name_map['stateAbbr'] = '省份简称'
    name_map['legalPersonId'] = '法人ID'
    name_map['legalPersonName'] = '法人姓名'
    # name_map['compCode'] = 'debug:公司Code'
    # print('col', df.columns)
    # 持股比例    sy_cd_ms_sh_gs_shlist_new.holdRatio  
        # 通过 cName 先与 sy_cd_ms_base_gs_comp_info_new 关联，查询 compCode
        # 之后通过 compCode 与 sy_cd_ms_sh_gs_shlist_new 关联
    df = gs_shlist(key='compCode',full_data=True
        ).append_fields_by_keys(df, 'compCode', 
            ['holdRatio','shId','shTypeCode','shName'])
    name_map['holdRatio'] = '持股比例'
    # name_map['shTypeCode'] = 'debug:持股类型'
    # 股东名称    sy_cd_ms_base_gs_comp_info_new.compName  见注1
    # 注1：
    # 1、通过 cName 与 sy_cd_ms_base_gs_comp_info_new.compName 关联,获取 compCode  
    # 2、compCode 与 sy_cd_ms_sh_gs_shlist_new.`compCode` 关联，获取 shId,shTypeCode,shName
    # 3、if shTypeCode=2时， shId 与 sy_cd_ms_base_gs_comp_info_new.compCode 关联，获取 compName 即为股东名
    # ELSE 直接使用 sy_cd_ms_sh_gs_shlist_new.shName 作为股东名
    df1 = df[df['shTypeCode']!=2]
    name_map['shName'] = '股东名称'
    
    df2 = df[df['shTypeCode']==2]
    del df2['shName']
    # df2 = gs_comp_info.copy(key='compCode',fields ="compName,compCode".split(','),full_data=True
    # ).append_fields_by_keys(df2, 'shId', 
    #     ['compName as shName'])
    if 'ugly fix':
        print('df2.columns', df2.columns)
        # df2['compName2'] = df2['compName']
        # del df2['compName']
        df2 = gs_comp_info.copy(key='compCode',fields ="compName,compCode".split(','),full_data=True
        ).append_fields_by_keys(df2, 'shId', 
            ['compName'])
        df2['shName'] = df2['compName']
        # df2['compName'] = df2['compName2']
    df_list.append(df1)
    df_list.append(df2)
    # print('df1', df1)
    # print('df2', df2);exit()
    
    # print(df);exit()

df = pandas.concat(df_list, axis=0)
df.rename(columns=name_map, inplace=True)
df = df.loc[:,list(name_map.values())]
file = "/shiye_data/chd_test/Extract_file/20220329_px_task1.xlsx"
print('write', file)
with pandas.ExcelWriter(file) as writer:
    # hp1.add_sheet(writer)
    df.to_excel(writer, sheet_name='sheet1', index=False)
