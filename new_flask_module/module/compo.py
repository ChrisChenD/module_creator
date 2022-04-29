#!/usr/bin/env python3

import copy
class Compo_common:
    @staticmethod
    def to_dict(self):
        if not isinstance(self, Compo_common):
            return self
        r = dict()
        for k,v  in self.kwargs.items():
            if isinstance(v, Compo_common):
                v = Compo_common.to_dict(v)
            if isinstance(v, list):
                v = [Compo_common.to_dict(e) for e in v]
            r[k] = v
        r['c'] = self.__class__.__name__
        return r
    # def __init__(self, **kwargs):
    #     self.kwargs = dict(
    #         c = self.__class__.__name__,
    #     )
    #     self.init(**kwargs)
    # def init(self, **kwargs):pass
class Com:
    class P(Compo_common):
        def __init__(self, cls_name, value): 
            self.kwargs = dict(cls_name=cls_name, value=value)
    class Table(Compo_common):
        def __init__(self, cls_name, cls_name_body, body): 
            self.kwargs = dict(
                cls_name=cls_name,
                cls_name_body=cls_name_body,
                body=body
            )
    class Line(Compo_common):
        def __init__(self, cls_name, fields): 
            self.kwargs = dict(
                cls_name=cls_name,
                fields=fields
            )






