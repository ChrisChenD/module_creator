#!/usr/bin/env python3

import copy
from module.module_base import Module_base, module_info, cls_default
class Com_common(Module_base):
    def call_param_func(self, idx__, func_name__, fix_kwargs, **ext_kwargs):
        # idx, func_name, params = func_info
        kwargs = copy.deepcopy(fix_kwargs)
        kwargs.update(ext_kwargs)
        print('idx__', idx__, 'func_name', func_name__)
        obj = self.get_obj_by_id(idx__)
        func = getattr(obj, func_name__)
        # func = eval(func)
        # assert isinstance(params, dict)
        return func(**kwargs)


class Com:
    @module_info.registry_terminator
    class Com_List(Com_common):
        '多行'
        @staticmethod
        def m(): return dict(
            e_list=list
        )
        def init(self, e_list, cls_name=cls_default):
            self.e_list = e_list
            self.cls_name = cls_name

        @classmethod
        def compo_js(cls_):
            class_name = cls_.__name__
            return f"""
function {class_name}(self){{
    return <div {cls_.base_attr(obj='self')}>
        {{self.e_list.map(
            (e, idx)=> {{
                e.call = self.call
                return <Auto_type {{...e}} key={{idx}}/>
            }}
        )}}
    </div>
}}
            """.strip()
    
    @module_info.registry_terminator
    class Com_Line(Com_common):
        '一行'
        @staticmethod
        def m(): return dict(
            e_list=list
        )
        def init(self, e_list, cls_name=cls_default):
            self.e_list = e_list
            self.cls_name = cls_name

        @classmethod
        def compo_js(cls_):
            class_name = cls_.__name__
            return f"""
function {class_name}(self){{
    return <div className='flex {{self.cls_name}}' key={{self.idx}}>
        {{self.e_list.map(
            (e, idx)=> {{
                e.call = self.call
                return <Auto_type {{...e}} key={{idx}}/>
            }}
        )}}
    </div>
}}
            """.strip()
    
    @module_info.registry_terminator
    class Com_Table(Com_common):
        '一行'
        @staticmethod
        def m(): return dict(
            e_list=list
        )
        def init(self, e_list, cls_name=cls_default):
            self.e_list = e_list
            self.cls_name = cls_name

        @classmethod
        def compo_js(cls_):
            class_name = cls_.__name__
            return f"""
function {class_name}(self){{
    return <table 
    className="table-fixed bg-sky-100" key={{self.idx}}>
        <thead>
        </thead>
        <tbody className='bg-stone-100' key='table_info1'>
            {{self.e_list.map(
                (line, line_idx) => <tr key={{line_idx}}>
                    {{line.map(
                        (e, e_idx)=>{{
                            e.call = self.call
                            return <th key={{e_idx}}>
                                <Auto_type {{...e}} key={{e_idx}}/>

                            </th >
                        }}
                    )}}
                </tr>
            )}}
        </tbody>
    </table>
}}
            """.strip()
            # <table className="table-fixed bg-sky-500" key='table'>
            #     <thead>
            #     </thead>
            #     <tbody className='bg-sky-101' key='table_info1'>
            #         {<TrRecord.html {...comment_param}></TrRecord.html>}
            #         {<TrRecord.html {...field_param}></TrRecord.html>}
            #         {<TrRecord.html {...select_param}></TrRecord.html>}
            #         {<TrRecord.html {...cond_param}></TrRecord.html>}
            #         {/* {TrRecord.html(comment_param)} */}
            #     </tbody>
            # </table>



    @module_info.registry_terminator
    class Com_P(Com_common):
        @staticmethod
        def m(): return dict(
            value=str
        )
        def init(self, value, cls_name=cls_default):
            self.value = value
            self.cls_name = cls_name
        @classmethod
        def compo_js(cls_):
            class_name = cls_.__name__
            # var params = data.params
            return f"""
function {class_name}(self){{
    return <p {cls_.base_attr(obj='self')}>{{self.value}}</p>
}}
            """.strip()
    
    @module_info.registry_terminator
    class Com_Button(Com_common):
        @staticmethod
        def m(): return dict(
            value=str
        )
        def init(self, value, onClick, cls_name=cls_default):
            self.value = value
            self.onClick_recall = onClick
            self.cls_name = cls_name
        def onClick(self, *params):
            # self.recall(*params)

            new_module = self.call_param_func(*self.onClick_recall)# (*params)
            return new_module

        @classmethod
        def compo_js(cls_):
            class_name = cls_.__name__
            # var params = data.params
            return f"""
function {class_name}(self){{
    return <button {cls_.base_attr(obj='self')} onClick={{
        self.call({{
            "idx":self.idx,
            "method":"onClick",
            "params":[]
        }})
    }}>{{self.value}}</button>
}}
            """.strip()
    
    @module_info.registry_terminator
    class Com_text(Com_common):
        @staticmethod
        def m(): return dict(
            text=str
        )
        def init(self, text, onEnter, cls_name=cls_default):
            self.text = text
            # self.default_holder = default_holder
            self.onEnter_recall = onEnter
            self.cls_name = cls_name
        def onEnter(self, *params):
            # self.recall(*params)
            self.text = params[0]
            new_module = self.call_param_func(*self.onEnter_recall, text=self.text)# (*params)
            return new_module

        @classmethod
        def compo_js(cls_):
            class_name = cls_.__name__
            # var params = data.params
            return f"""
function {class_name}(self){{
    const onkeyup_action = (event) => {{
        if(event.key=='Enter'){{
            event.preventDefault()
            const text = document.getElementById(self.idx).value;
            self.call({{
                "idx":self.idx,
                "method":"onEnter",
                "params":[text, ]
            }})()
        }}
    }}
    return <input {cls_.base_attr(obj='self')}
        id={{self.idx}}
        placeholder={{self.text}}
        onKeyUp={{onkeyup_action}}
    />
}}
            """.strip()

    @module_info.registry_terminator
    class Com_textarea(Com_common):
        @staticmethod
        def m(): return dict(
            text=str,
            rown=int,
            coln=int
        )
        # def init(self, text, onEnter, rown=40, coln=80, cls_name=cls_default):
        def init(self, text, rown=40, coln=80, cls_name=cls_default):
            self.text = text
            self.rown = rown
            self.coln = coln
            # self.default_holder = default_holder
            # self.onEnter_recall = onEnter
            self.cls_name = cls_name
        # def onEnter(self, *params):
        #     # self.recall(*params)
        #     self.text = params[0]
        #     new_module = self.call_param_func(*self.onEnter_recall, text=self.text)# (*params)
        #     return new_module

        @classmethod
        def compo_js(cls_):
            class_name = cls_.__name__
            # var params = data.params
            return f"""
function {class_name}(self){{
    const onkeyup_action = (event) => {{
        if(event.key=='Enter'){{
            event.preventDefault()
            const text = document.getElementById(self.idx).value;
            self.call({{
                "idx":self.idx,
                "method":"onEnter",
                "params":[text, ]
            }})()
        }}
    }}
    return <textarea {cls_.base_attr(obj='self')}
            id={{self.idx}}
            rows={{self.rown}} cols={{self.coln}}
            defaultValue={{self.text}}
            />
}}
            """.strip()



class Module_base_debug(Module_base):
    '用于调试, 设置一个默认compo到 类中'
    @staticmethod
    def m(): 
        return dict(
        debug_=Com.Com_P,
    )
    def __init__(self, father, *args, **kwargs):
        '如果设置 m(), 就不要采用debug模式, 去继承 Module_base'
        super().__init__(father, *args, **kwargs)
        self.debug_.init(self.__class__.__name__)

    # def init(self, note):
    #     self.region_name.init(self.__class__.__name__)




