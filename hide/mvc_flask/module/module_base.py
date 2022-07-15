cls_default = 'bg-stone-700 border-4 text-white'

class Module_info:
    def __init__(self):
        self.cls_list = []
        self.compo_list = []
    def registry(self, class_):
        'registry js class'
        self.cls_list.append(class_)
        return class_

    def registry_terminator(self, class_):
        'registry compo function'
        # 注册compo 类
        self.compo_list.append(class_)
        return class_
module_info = Module_info()

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
        self.init_from_m()
        if args != tuple() or kwargs != dict():
            self.init(*args, **kwargs)
    def get_obj_by_id(self, idx):
        obj = self.root.idx_maker[idx]
        return obj

    def init_from_m(self):
        for member_name, cls_ in self.m().items():
            if cls_ in [list, dict, str, int]:
                setattr(self, member_name, cls_())
            else:
                setattr(self, member_name, cls_(self))

    def init(self, *args, **kwargs):
        'how to set class members'
        pass
    

    @staticmethod
    def m():
        'js.members'
        'member: cls(self)'
        return dict()
    @classmethod
    def m_ext(cls_):
        '扩展member, 增加默认字段'
        return [
            'idx', 'cls_name', 'cls_type_'
        ]+list(cls_.m().keys())
    
    @staticmethod
    def base_attr(obj='self'): 
        return f"key={{{obj}.idx}} className={{{obj}.cls_name}}"

    @classmethod
    def v(cls_):
        # 'js.view'
        # name = cls_.__name__
        # return f"""<p {cls_.base_attr()}>[class: {name}]</p>"""
        def compo_name(cls_):
            compo_name = cls_.__name__
            if not compo_name.startswith('Com_'):
                compo_name = f'{compo_name}.view'
            return compo_name
        member_list = [
            f'<{compo_name(cls_)} {{...self.{member}}}></{compo_name(cls_)}>'
            for member,cls_ in cls_.m().items()
        ]
        member_list = ('\n'+" "*12).join(member_list)
        return f"""
        <div {cls_.base_attr()}>
            {member_list}
        </div>
        """.strip()
    def c(self):
        'not use'
        pass
    def to_json_dict(self):
        def to_dict_simple(obj):
            if isinstance(obj, Module_base):
                return obj.to_json_dict()
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
        r['cls_name'] = getattr(self, 'cls_name', cls_default)
        return r

    def js_code(self):
        cls_name = self.__class__.__name__
        member_set = ('\n'+' '*8).join([ 
            f"this.{member} = data.{member}"
            for member in self.m_ext()+['call']])

        member_set_call = ('\n'+' '*8).join([ 
            f"self.{member}.call = self.call"
            for member in self.m().keys()])

        return f"""
export class {cls_name} {{
    constructor(data) {{
        {member_set}
    }}

    static view(data){{var self = new {cls_name}(data)
        {member_set_call}
        return {self.v()}
    }}
}}
        """


class Module_root(Module_base):
    @classmethod
    # def default_module(cls_, plan_name='for_js'):
    def default_module(cls_, *args, **kwargs):
        module = cls_(None)
        module.init(*args, **kwargs)
        return module#, plan_name=plan_name)# root=None

    def call(self, params):
        # "idx":self.idx,
        # "method":"onClick",
        # "params":""
        idx = params['idx']
        method = params['method']
        func_params = params['params']
        print('call:', params)
        # params is [p1, p2, ...]
        obj = self.get_obj_by_id(idx)
        module = getattr(obj, method)(*func_params)
        if module is not None:
            # module
            print("module is not None! ")
            return module
        return self
    @property
    def f_name(self):
        return f'mvc_flask/module/plan_history/{self.name}.module'

    def SAVE_MODULE(self):
        module = self
        import pickle
        with open(self.f_name, 'wb') as f:
            pickle.dump(module, f)
        return module
    def LOAD_MODULE(self):
        module = self
        import pickle
        try:
            with open(self.f_name, 'rb') as f:
                module = pickle.load(f)
                print(f'load plan [{self.name}] success!')
        except:
            print(f'load plan [{self.name}] fail!')
            import traceback;print(traceback.format_exc())
        return module


