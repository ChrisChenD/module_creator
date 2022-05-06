#!/usr/bin/env python3

import copy
# class Compo_common:
#     @staticmethod
#     def to_dict(self):
#         if not isinstance(self, Compo_common):
#             return self
#         r = dict()
#         for k,v  in self.kwargs.items():
#             if isinstance(v, Compo_common):
#                 v = Compo_common.to_dict(v)
#             if isinstance(v, list):
#                 v = [Compo_common.to_dict(e) for e in v]
#             r[k] = v
#         r['c'] = self.__class__.__name__
#         return r
    # def __init__(self, **kwargs):
    #     self.kwargs = dict(
    #         c = self.__class__.__name__,
    #     )
    #     self.init(**kwargs)
    # def init(self, **kwargs):pass
# class Common(Compo_common)

# class Module_ids:
#     def __init__(self):
#         self.ids_map = {}
#     def set(self, idx, obj):
#         self.ids_map[idx] = obj
#     def have(self, idx):
#         return idx in self.ids_map

        
# class Compo_common:
#     module_ids = Module_ids()
#     # def reset_ids
    
#     def __init__(self, **kwargs):
#         self.set_idx()
#         self.init(**kwargs)

#     def set_idx(self):
#         '给每个节点设置唯一id'
#         idx = 0
#         while 1:
#             if self.module_ids.have(idx):
#                 idx += 1
#                 continue
#             break
#         self.idx = idx
#         self.module_ids.set(idx, self)
    
#     def __init__(self, cls_name, **kwargs):
#         self.set_idx()
#         self.cls_name = cls_name
#         self.init(**kwargs)
#     def attr(self):
#         return f'className="{self.cls_name}" key="{self.idx}"'

# class Com:
#     class P(Compo_common):
#         def init(self, value): 
#             self.value = value
#         def json(self):
#             return f"""
# <p {self.attr()}>{{self. value}}</p>
#             """.strip()
#     class Div(Compo_common):
#         def init(self, e_list): 
#             self.e_list = e_list
#         def json(self):
#             e_list = self.e_list
#             return f"""
# <div {self.attr()}>
#     {self. e_list}
# </div>
#             """.strip()

#         # def __init__(self, cls_name, rows): 
#         #     self.kwargs = dict(
#         #         cls_name=cls_name,
#         #         rows=rows
#         #     )
    
    
    
    
#     class Table(Compo_common):
#         def __init__(self, cls_name, cls_name_body, body): 
#             self.kwargs = dict(
#                 cls_name=cls_name,
#                 cls_name_body=cls_name_body,
#                 body=body
#             )
#     class Line(Compo_common):
#         def __init__(self, cls_name, fields): 
#             self.kwargs = dict(
#                 cls_name=cls_name,
#                 fields=fields
#             )
#     class Union(Compo_common):
#         def __init__(self, cls_name, rows): 
#             self.kwargs = dict(
#                 cls_name=cls_name,
#                 rows=rows
#             )
#     class Eval(Compo_common):
#         def __init__(self, cls_name, obj):
#             self.kwargs = dict(
#                 cls_name=cls_name,
#                 obj=obj
#             )

from module.module_base import Module_base

class Com:
    class p(Module_base):
        def init(self, value, cls_name=''):
            self.value = value
            self.cls_name = cls_name
        @classmethod
        def v(cls_):
            return f"<p {cls_.base_attr()}>{{self.value}}</p>"
    class List(Module_base):
        def init(self, e_list, cls_name=''):
            self.e_list = e_list
            self.cls_name = cls_name
        @classmethod
        def v(cls_):
            return f"""<div {cls_.base_attr()}>
                {{self.e_list.map(
                    (e, idx)=> Auto_view(e)
                )}}
            </div>"""
    
    # class List(Com_base):
    #     def init(self, e_list, cls_name=''):
    #         self.e_list = e_list
    #         # self.value = value
    #         self.cls_name = cls_name
    #     def m(self): return dict(
    #         e_list=
    #     )
    #     def v(self):
    #         return f"""<div {self.base_attr()}>{{self.e_list.map(
    #             (e, index) => 
    #         )}}</div>"""
        





