
class Traversed_module:
    @staticmethod
    def m():return ['member1', 'member2', 'member3']
    def traverse(self):
        for module in self.traverse_sub_module():
            yield module
        yield self

    def traverse_sub_module(self):
        for member_name in self.m().keys():
            obj = getattr(self,member_name)
            if isinstance(obj, Traversed_module):
                for obj_sub in obj.traverse_sub_module():
                    yield obj_sub
                yield obj
            if isinstance(obj, list):
                for obj_sub in obj:
                    if isinstance(obj_sub, Traversed_module):
                        for module in obj_sub.traverse_sub_module():
                            yield module
                        yield obj_sub
            if isinstance(obj, dict):
                for obj_sub in list(obj.values()):
                    if isinstance(obj_sub, Traversed_module):
                        for module in obj_sub.traverse_sub_module():
                            yield module
                        yield obj_sub


class Root_idx_map(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cur_idx = 0
    def registry(self, obj):
        '给每个节点设置唯一id'
        obj.idx = self.cur_idx
        self[obj.idx] = obj
        self.cur_idx += 1

class Module_base(Traversed_module):
    def __init__(self, father, *args, **kwargs):
        self.father = father
        self.root = None
        # self.cls_type = self.__class__.__name__
        if father is None:
            self.root = self
            self.idx_maker = Root_idx_map()
            self.idx_maker.registry(self)
        else:
            self.root = self.father.root
            # 注册唯一 idx
            self.root.idx_maker.registry(self)
        # 初始化
        if args != tuple() or kwargs != dict():
            self.init(*args, **kwargs)
        
    def init(self, *args, **kwargs):
        'how to set class members'
        pass
        
    @staticmethod
    def m():
        'js.members'
        'member: cls(self)'
        return dict()
    
    @staticmethod
    def base_attr(): 
        return f"key={{self.idx}} className={{self.cls_name}}"

    @classmethod
    def v(cls_):
        'js.view'
        name = cls_.__name__
        return f"""<p {cls_.base_attr()}>[class: {name}]</p>"""
    def c(self):
        'not use'
        pass
    def to_dict(self):
        def to_dict_simple(obj):
            if isinstance(obj, Module_base):
                return obj.to_dict()
            if isinstance(obj, list):
                return list(
                    to_dict_simple(sub_obj)
                    for sub_obj in obj
                )
            if isinstance(obj, dict):
                return dict(
                    (k,to_dict_simple(v))
                    for k,v in obj.items()
                )
            return obj
            
        r = dict()
        for member_name in self.m().keys():
            member = getattr(self, member_name)
            r[member_name] = to_dict_simple(member)
        r['cls_type_'] = self.__class__.__name__
        r['idx'] = self.idx
        return r

    def js_code(self):
        cls_name = self.__class__.__name__
        member_set = ('\n'+' '*8).join([ 
            f"this.{member} = data.{member}"
            for member in self.m().keys()])

        return f"""
export class {cls_name} {{
    constructor(data) {{
        {member_set}
    }}

    static view(data){{var self = new {cls_name}(data)
        return {self.v()}
    }}
}}
        """
