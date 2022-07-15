#!/usr/bin/env python3
from multiprocessing.sharedctypes import Value
import pandas
import datetime

class Module:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, "_"+key, value)
    def __call__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, "_"+key, value)
        return self
    @property
    def _name(self):
        return self.__class__.__name__
    def _demo():
        class Db1(Db):
            class Tb1(Table):
                class C1(Column):
                    pass
        c1 = Db1.Tb1.C1(inplace=True)

class Db:
    @property
    def engine(self):
        if not hasattr(self.__class__, '_engine'):
            setattr(self.__class__, '_engine', SampleEngine(
                self.__class__
            ))
        return self._engine
    
class Table(Module):
    # @property
    # def _db(self):
    #     # self._path = "db135.sy_cd_me_buss_compete_products"
    #     self.init()
    #     dbcls = eval("self."+self._table._path.rsplit('.', 1)[0])
    #     return dbcls()
    @property
    def _table(self):
        return self

    @property
    def _df(self):
        return self._table._db.engine[
            self._table._name,
            self._table._select, 
            self._table._cond
        ].df

    def _scan(self, *s_list):
        "扫描, 看看哪个字段"
        
        for s in s_list:
            r = []
            for col in [getattr(self._table.__class__, col_name)()
                for col_name in self._table._cols.split(',')
                ]:
                r.append(col._scan_col(s))
            r = list(filter(None, r))
            print(f'[{s}] result number: {len(r)}')
            for c in r:
                c = c.split(':')[0]
                info = f"{s}: {c}"
                print(info)


class Column(Table):
    # @property
    # def _table(self):
    #     self.init()
    #     dbcls = eval("self."+self._path.rsplit('.', 1)[0])
    #     return dbcls()
    def _scan_col(self, s):
        if s in self._name or s in self._cname:
            return str(self)
        return None
    def __str__(self):
        return f'[{self._cname}]{self._name}<{self._vtype}>: {self._path}'


class SampleEngine:
    def __init__(self, db):
        self.db = db
        self.tb_name, self.select, self.cond = [None,]*3
    def __getitem__(self, slice_):
        self.tb_name, self.select, self.cond = slice_
        return self
    @property
    def df(self):
        self.sql = f"select {self.select} from {self.tb_name} where {self.cond}"
        print('sql:', self.sql)
        df = pandas.DataFrame(self.db._sample)
        return df


