#!/usr/bin/env python3 

class Dict_op:
    def to_dict(self):
        d = dict()
        for member in dir(self):
            if not member.startswith('_'):
                d[member] = getattr(self, member)
        return d
    def from_dict(self, d):
        for member,member_value in d.items():
            setattr(self, member, member_value)
    member_list = []
    # def __init__(self, *args):
    #     for i,member_name in enumerate(self.member_list):
    #         setattr()


class Functor:
    class _1_read_mysql(Dict_op):
        def __str__(self):
            r = """
            def read_mysql():
                df_chunks = read_mysql(
                    mysql_chain = {self.mysql_chain},
                    cond = {self.cond},
                    select = {self.select}
                )
                for chunk in df_chunks:
                    yield df
            """.strip()
            return r
            # # json
            # {
            #     "mysql_chain":str,
            #     "cond":list,
            #     "select":list,
            # }