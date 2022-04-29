#!/usr/bin/env python3

import pymysql
import sqlalchemy
import pandas

class Db:
    "user:password@127.0.0.1:3306/database_name"
    def __init__(self, info_string):
        self.info_string = info_string
    @property
    def config(self):
        info = self.info_string
        config = dict()
        config['user'], info = info.split(':', 1)
        config['password'], info = info.split('@', 1)
        config['host'], info  = info.split(':')
        config['port'], config['database']  = info.split('/')
        config['port'] = int(config['port'])
        return config
    @property
    def client_cmd(self):
        config = self.config
        return [
            'mysql -h {host} -P {port} -u {user} -D {database} -p'.format(**config),
            config['password']
        ]

class ReadMysql:
    'Read_mysql'
    def __init__(self, config_string, chunksize=1000, sqlprint=False, timeout=None):
        # print('chunksize', chunksize)
        self.timeout = timeout
        self.sqlprint = sqlprint
        self.chunksize = chunksize
        self.config = config_string
        self.cursor, self.db = None, None
        self.connect()
    def __del__(self): self.disconnect()
    def connect(self):
        self.db = pymysql.connect(**Db(self.config).config, read_timeout=self.timeout)
        self.cursor = self.db.cursor()
    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()
    
    def __call__(self, sql):
        #sql = "INSERT INTO userinfo(username,passwd) VALUES('jack','123')"
        try:
            self.cursor.execute(sql)
            r = self.cursor.fetchall()
            return r
        except:
            print('Mysql Query#:', sql)
            import traceback;print(traceback.format_exc())

    def show(self, sql):
        r = self(sql)
        print(r)
    @property
    def table_list(self):
        'list all tables in database'
        r = self('show tables;')
        return [record[0] for record in r]
    
    def create_info(self, table_name):
        'list all fields infomation'
        # print('debug', 'table_name', table_name)
        r = self(f'show create table {table_name}')
        # print('debug', 'r', r)
        name, create_sql, *rest = r[0]
        # cols = create_sql.split('(', 1)[1].rsplit(')', 1)[0]
        # cols = cols.split(',')
        # cols = [col_info.strip() for col_info in cols]
        # return cols
        return create_sql

    def demo_1():
        # mysql = ReadMysql("test:test@127.0.0.1:3306/test")
        mysql = ReadMysql('kf2_poc:shiye1805A@127.0.0.1:30152/seeyii_assets_database')
        for table_name in mysql.table_list:
            print(table_name, mysql.create_info(table_name))
        r = mysql('select * from test1')
        print(r)
        print(list(zip(*r)))
        
    @property
    def df(self):
        # engine = sqlalchemy.create_engine(f'mysql+pymysql://{self.config}')
        if self.sqlprint:
            print('sql', self.sql)
        # df = pandas.read_sql_query(self.sql, engine)
        df = pandas.read_sql_query(self.sql, self.db)
        return df

    @property
    def df_chunks(self):
        # print('sql', self.sql)
        # df_chunk_iter = pandas.read_sql_query(self.sql, self.db, chunksize=self.chunksize)
        # return df_chunk_iter
        # import pandas.io.sql as psql
        # chunk_size = 10000
        # offset = 0
        id_base = 0
        # dfs = []
        
        while True:
            print('id_base', id_base)
            sql = f"{self.sql} and id > {id_base} order by id limit {self.chunksize} "#  % (self.chunk_size, offset) 
            if 'id' not in self.fields:
                old_fields = self.fields
                self.fields = old_fields + ',id'
                sql = f"{self.sql} and id > {id_base} order by id limit {self.chunksize} "#  % (self.chunk_size, offset) 
                self.fields = old_fields
            print('sql', sql)
            new_df = pandas.read_sql_query(sql, self.db)
            # print(new_df)
            id_base = new_df.iloc[-1]['id']
            print('id_base:', id_base)
            yield new_df
            if len(new_df) < self.chunksize:
                break
            
        # full_df = pd.concat(dfs)

    @property
    def sql(self):
        return f'select {self.fields} from {self.table_name} where {self.cond}'
    def __getitem__(self, _slice):
        "[table_name, fields, where/cond]"
        self.table_name, self.fields, self.cond = _slice
        return self
    def demo_2():
        mysql = ReadMysql("test:test@127.0.0.1:3306/test")
        df = mysql['test1', 'id,name', 'id > 1'].df
        # show df
        df.info()
        print(df)
    @property
    def dict(self):
        '把mysql查询结果, 制作成dict: {field1:field2}'
        # r =  dict()
        # for idx, row in self.df.iterrows():
        #     r[row[0]] = row[1]
        # return r
        return dict(
            (row[0], row[1])
            for idx, row in self.df.iterrows()
        )
    @property
    def set(self):
        return set(
            row[0]
            for idx, row in self.df.iterrows()
        )
    @property
    def series(self):
        # first col
        return self.df
    
    def table_info(self, table_name):
        create_sql = self.create_info(table_name)
        return Table_info(create_sql)


def Encode(s, pair=('(', ')'), mid_func=lambda mid:mid.replace(',', '?')):
    "把(,) 转化成 (?)"
    lc, rc = pair
    new_s = ''
    while len(s) > 0:
        if lc not in s:
            return new_s + s
        a, s = s.split(lc, 1)
        mid, b = s.split(rc, 1)
        mid = mid.replace(',', '?')
        s = b
        new_s += f"{a}{lc}{mid}{rc}"
    return new_s

class Table_info:
    class col_info:
        def __init__(self, create_sql=''):
            self.create_sql = create_sql
            self.name = ''
            self.type = ''
            self.rest = ''
            self.comment = ''
            self.parse()

        def __str__(self) -> str:
            return f'[{self.comment}]{self.name}<{self.type}>..{self.rest}'
        def parse(self):
            try:
                sql = self.create_sql
                if sql == '':
                    return 
                sql = sql.strip()
                sql = Encode(sql, ('(', ')'), lambda mid:mid.replace('?', ','))
                sql = Encode(sql, ("'", "'"), lambda mid:mid.replace('?', ','))

                if "COMMENT" in sql:
                    sql, self.comment = sql.split("COMMENT", 1)
                    self.comment = self.comment.strip()[1:-1]

                self.name, self.type = sql.split(' ', 1)
                if ' ' in self.type:
                    self.type, self.rest = self.type.split(' ', 1)
            except:
                print('sql', sql);raise 'error'
    
    default_dismiss_col = ['dataStatus', 'isValid', 'createTime', 'updateTime', 'id',
        'modifyTime', 'fingerId'
    ]
    # default_dismiss_col = ['dataStatus', 'isValid', 'createTime', 'updateTime']
    # Table_info(sql, default_dismiss_col)
    def __init__(self, create_sql='', dismiss=None):
        self.create_sql = create_sql
        self.table_name = ''
        self.comment = ''# cn name
        self.col_list = []
        self.parse()
        self.dismiss_col = dismiss if dismiss is not None else self.default_dismiss_col
    def parse(self):
        try:
            sql = self.create_sql
            # print(sql)
            # cn （） > en ()
            sql = sql.replace('（', '(').replace('）', ')')
            if 'CREATE TABLE' not in sql:
                return 
                # case1: sql=''  not init
                # case2: table is a view
            sql = sql.replace('`', '')
            self.table_name, sql = sql.split('(', 1)
            self.table_name = self.table_name.strip().split(' ')[-1]
            # sql, comment = sql.rsplit(')', 1)
            sql, comment = sql.rsplit('ENGINE', 1)
            sql = sql.rsplit(')', 1)[0]
            
            if 'COMMENT=' in comment:
                self.comment = comment.strip()
                self.comment = self.comment.rsplit('COMMENT=', 1)[1][1:-1]#
            sql = Encode(sql, ('(', ')'), lambda mid:mid.replace(',', '?'))
            sql = Encode(sql, ("'", "'"), lambda mid:mid.replace(',', '?'))
            
            self.col_list = [self.col_info(col) for col in sql.split(',')]
        except:
            import traceback
            print(self.create_sql);print(traceback.format_exc());
            # exit()
            pass# continue
    @property
    def col_dict(self):
        r = dict([(col.name,col.comment) for col in self.col_list])
        for key in ['PRIMARY', 'KEY', 'UNIQUE'] + self.dismiss_col:
            if key in r:
                del r[key]
        
            #     def dismiss_column(self):
            # for key in ['dataStatus', 'isValid', 'createTime', 'updateTime', 'id']:
            #     if key in col_dict:
            #         del col_dict[key]
        return r
        # PRIMARY', 'UNIQUE', 'KEY', 'KEY
    @property
    def cols(self):
        return list(self.col_dict.keys())
        # r = [col.name for col in self.col_list]
    @property
    def cols_cn(self):
        return list(self.col_dict.values())
        # return [col.comment for col in self.col_list]

    def demo3():
        db, table = 'select_company_2:shiye1805A_select_company_2@pc-2zestdjva92am7na5.rwlb.rds.aliyuncs.com:3306/seeyii_assets_database', 'sy_cd_ms_base_comp_list'
        table_info = ReadMysql(db).table_info(table)
        table_cn = table_info.comment
        col_dict = table_info.col_dict
        print('table_cn', table_cn)
        print('col_dict', col_dict)
    
    
if __name__ == '__main__':
    # ReadMysql.demo_1()
    # ReadMysql.demo_2()
    Table_info.demo3()

