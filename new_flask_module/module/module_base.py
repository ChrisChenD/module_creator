#!/usr/bin/env python3
import copy
from os import access
# from plan2_module.mysql_utils import ReadMysql
from new_flask_module.module.mysql_utils import ReadMysql

class Module_common:
    members__ = {}
    # default__ = {}
    # @staticmethod
    def access__(self): return None
    # ___access = None
    def init(self, **kwargs):pass
    def __init__(self, **kwargs):
        for member,member_value in self.members__.items():
            if member in kwargs:
                member_value = kwargs[member] 
            setattr(self, member, member_value)
        self.init(**kwargs)
    
    def to_dict(self):
        return Module_common.to_dict_(self)

    @classmethod
    def to_dict_(cls_, obj):
        '序列化'
        if isinstance(obj, Module_common):
            print('obj', obj)
            print('obj.__class__', obj.__class__)
            # print('')
            # print('obj.__class__', obj.__class__)
            r1 = [
                ('___class',obj.__class__.__name__)
            ]
            print('obj.members__', obj.members__)
            r2 = [
                (member_name, cls_.to_dict_(getattr(obj, member_name)) if hasattr(obj, member_name) else None)
                for member_name in obj.members__
            ]
            return dict(r1+r2)
        else:
            if isinstance(obj, list):
                return [cls_.to_dict_(member) for member in obj]
            elif isinstance(obj, dict):
                return dict([
                    (k,cls_.to_dict_(member)) for k,member in obj.items()
                ])
            else:
                if hasattr(obj, 'to_dict'):
                    return obj.to_dict(obj)
                else:
                    print('direct obj:', obj)
                    return obj
    
    @classmethod
    def load_dict(cls_, d_obj):
        '从序列化数据中创造/初始化'
        if not cls_._is_legal_obj(d_obj):
            raise Exception(f'{__file__}: load Fail')
        recovered_d_obj = dict()
        for k,v in d_obj.items():
            recovered_v = v
            if cls_._is_legal_obj(v):
                recovered_v = cls_.load_dict(v)
            recovered_d_obj[k] = recovered_v
        return cls_._recover_cls(**recovered_d_obj)
    
    @classmethod
    def _is_legal_obj(cls_, d_obj):
        if (not isinstance(d_obj, dict)) or '_class_' not in d_obj:
            return False
        return True
    @classmethod
    def _recover_cls(cls_, d_obj):
        if not cls_._is_legal_obj(d_obj):
            raise Exception(f'{__file__}: load Fail')
        _class_ = d_obj['___class']
        return _class_(**d_obj)
        # ('_class_',obj.__class__)
    def get_access(self, class_space):
        cur_cls = self.__class__# cls_
        access = []
        while 1:
            method = cur_cls().access__()
            if method is None:
                break
            access.append(method.link__)
            # cur_cls = eval(method.link__["class"])
            cur_cls = class_space[method.link__["class"]]
        return access
    
    # @classmethod
    def to_javascript(self, class_space):
        cls_ = self.__class__
        '直接把类转化成 js'
        set_members = [
            f"this.{member} = data.{member}" 
            for member in cls_.members__
        ]
        tab = ' '*4
        set_members = ('\n'+tab*2).join(set_members)
        class_name = cls_.__name__
        cur_cls = cls_
        access = []
        while 1:
            method = cur_cls().access__()
            if method is None:
                break
            access.append(method.link__)
            # cur_cls = eval(method.link__["class"])
            cur_cls = class_space[method.link__["class"]]
        access = str(access)
        # access = cls_().access__()
        # if access is not None:
        #     print('access', access, dir(access))
        #     access = access.link__
        # print(f'{class_name}.access: {access}')
        access_func = f"""
    backend_access(){{return {access}}}
        """.rstrip()
        call_list = [
            Js_maker.link_code(getattr(cls_, member_name))
            for member_name in dir(cls_)
            if (not member_name.startswith('_')) and Js_maker.is_link(
                getattr(cls_, member_name)
            )
        ]
        call_list = '\n'.join(call_list)
        return f"""
export class {class_name} {{
    constructor(data) {{
        {set_members}
    }}
    {access_func}
    {call_list}
    static html(data){{var self = new {class_name}(data);return self.view();}}
    view (){{ return <p>{class_name}</p> }}
}}
""".strip()




class Js_maker:
    '通过类装饰器, 注册所有js类'
    def __init__(self):
        self.cls_list = []
    def registry(self):
        def deco(cls_):
            self.cls_list.append(cls_)
            return cls_
        return deco
    def call_param(self, cls_):
        class_space = dict(
            (cls_.__name__, cls_)
            for cls_ in self.cls_list
        )
        access_param = cls_().get_access(class_space)
        return access_param
    @property
    def code(self):
        r = []
        class_space = dict(
            (cls_.__name__, cls_)
            for cls_ in self.cls_list
        )
        for cls_ in self.cls_list:
            r.append(f'\n// {cls_.__name__}')
            r.append(cls_().to_javascript(class_space))
        return '\n'.join(r)
    @staticmethod
    def set_link(func, class_name, func_name, params, is_router):
        func.link__ = {
            'class':class_name,
            'params':params,
            'is_router':is_router,
        }
        func.__name__ = "__link__"+func_name
        # func.cls = eval(func.link__['class'])
        return func
    @staticmethod
    def is_link(func):
        if callable(func) and func.__name__.startswith("__link__"):
            return True
        return False
    @staticmethod
    def link_code(func):
        # print('link_code', func.__name__)
        func_name = func.__name__[len('__link__'):]
        params = func.link__['params']
        is_router = func.link__['is_router']
        if is_router:
            return ''
        else:
            param_list = ', '.join(params)
            ret_set_param = [
                f"'{param}':{param}"
                for param in params
            ]
            ret_set_param = "{"+','.join(ret_set_param)+'}'
            # {
            #     'method':func_name,
            #     'params':[params]
            # }
            return f"""
    // call backend!
    {func_name}({param_list}){{
        return this.backend_access()+[{{
            'method':'{func_name}',
            'params':{ret_set_param}
        }}]
    }}
        """.rstrip()

    def registry_call(self, class_name, params, is_router=False):
        '增加 link, 声明一个函数如何调用'
        def deco(func):
            def new_func(*args, **kwargs):
                return func(*args, **kwargs)
            new_func = self.set_link(new_func, class_name, func.__name__, params, is_router)
            # print('registry_call:', new_func.link__)
            return new_func
        return deco
    
    def registry_router(self, class_name, params):
        return self.registry_call(class_name, params, is_router=True)


js_maker = Js_maker()



