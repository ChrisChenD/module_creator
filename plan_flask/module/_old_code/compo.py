#!/usr/bin/env python3

# from module.compo_html import Com_html
# from module.compo_canvas import Com_canvas as Com
import copy
from module.module_base import Module_base, module_info, cls_default
from plan_flask.module.functor.functor import genus_functors_param

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
    class Com_Functor(Com_common):
        'Functor2的引用'
        @staticmethod
        def m(): return dict(
            x=int,
            y=int,
            name=str,
            highlight=bool,
            select=bool,
        )
        def init(self, x, y, name, cls_name=cls_default):
            self.x, self.y = x, y
            self.name = name
            self.highlight = False
            self.select = False
            self.cls_name = cls_name
            self.functor_param = dict()
            # self.onMousedown_recall = onMousedown
        def onMousedown(self, *params):
            return self.call_param_func(
                self.root.canvas.idx,
                'onMousedown',
                dict(idx=self.idx)
            )
        def onMouseup(self, x, y):
            return self.call_param_func(
                self.root.canvas.idx,
                'onMouseup',
                dict(idx=self.idx, x=x, y=y)
            )
        def config_compose_list(self):
            # 1 算子名称
            # 2 备注（扩展名）
            # 3 参数
            # 4 详细描述
            # 5 代码(可修改)
            return [
                Com.Com_P(self, value=self.name),
                Com.Com_P(self, value='[备注（扩展名）]'),
                Com.Com_P(self, value='[参数]'),
                Com.Com_P(self, value='[详细描述]'),
                Com.Com_P(self, value='[代码(可修改)]'),
            ]
        
        @classmethod
        def compo_js(cls_):
            class_name = cls_.__name__
            return f"""
function {class_name}(self){{
    return <Functor2.view {{...self}}/>
}}
            """.strip()
    
    @module_info.registry_terminator
    class Com_Canvas(Com_common):
        'canvas简单版本'
        @staticmethod
        def m(): return dict(
            w=int,
            h=int,
            functor_list=list,
            link_table=list,
            link_flag=bool,
        )
        def init(self, w, h, functor_list, link_table, cls_name=cls_default):
            self.w, self.h = w, h
            self.functor_list = functor_list
            self.link_table = link_table
            self.link_flag = 0
            self.cls_name = cls_name
        def add_link(self, from_rank, to_rank):
            if self.link_flag == 1:
                self.link_bind(from_rank, to_rank)
            if self.link_flag == 2:
                self.link_unbind(from_rank, to_rank)
        def link_bind(self, from_rank, to_rank):
            print('link_bind!', from_rank, to_rank)
            if from_rank == to_rank:
                return
            if from_rank not in self.link_table:
                self.link_table[from_rank] = []
            if to_rank not in self.link_table[from_rank]:
                self.link_table[from_rank].append(to_rank)
                self.cancel_link_flag()
        def link_unbind(self, from_rank, to_rank):
            print('link_unbind!', from_rank, to_rank)
            if to_rank in self.link_table[from_rank]:
                self.link_table[from_rank] = [
                    rank
                    for rank in self.link_table[from_rank]
                    if rank != to_rank
                ]
                self.cancel_link_flag()

        def get_functor(self, idx):
            for functor in self.functor_list:
                if functor.idx == idx:
                    return functor
                    
        def dehighlight_functor(self):
            '反高亮'
            for functor in self.functor_list:
                functor.highlight = False
        def highlight_functor(self, functor_idx):
            '高亮/选中functor'
            functor = self.get_functor(functor_idx)
            functor.highlight = True
            self.highlight_functor_show_in_plan()
        def highlight_functor_show_in_plan(self):
            functor, idx = None,None
            for i,f in enumerate(self.functor_list):
                if f.highlight:
                    functor = f
                    idx = i
            plan = self.root
            plan.cur_functor.init(functor.config_compose_list())

            

        def select_functor(self, functor_idx):
            '对象被点击选中, 用来拖拽, 重定位判定'
            functor = self.get_functor(functor_idx)
            functor.select = True
        def deselect_functor(self):
            '反选中'
            for functor in self.functor_list:
                functor.select = False
        def move_functor_to(self, idx, x, y):
            functor = self.get_functor(idx)
            functor.x, functor.y = x, y
            

        def functor_rank_from_idx(self, idx):
            for rank,functor in enumerate(self.functor_list):
                if functor.idx == idx:
                    return rank
            return None

        def onMousedown(self, idx):
            '当link的时候传来连接两个functor的消息'
            assert self.link_flag != 0
            # 找到高亮算子, 被对方连接
            rank = self.functor_rank_from_idx(idx)
            from_rank = None
            for rank_i, functor in enumerate(self.functor_list):
                if functor.highlight == True:
                    from_rank = rank_i
            # 必须有高亮算子才可以连接
            assert rank is not None
            assert from_rank is not None
            self.add_link(from_rank, rank)
        
        def onMouseup(self, idx, x, y):
            print('onMouseup', 94)
            # self.dehighlight_functor()
            # self.deselect_functor()
            self.move_functor_to(idx, x, y)
            self.dehighlight_functor()
            self.highlight_functor(idx)
            

        def add_functor(self, kwargs):
            self.functor_list.append(
                Com.Com_Functor(self, **kwargs)
            )
        def del_highlight_functor(self):
            '图删除点, 需要连带删除边'
            highlight_rank_id = None
            for rank, functor in enumerate(self.functor_list):
                if functor.highlight:
                    highlight_rank_id = rank
                    break
            if highlight_rank_id is not None:
                switch_rank_dict = dict([
                    (highlight_rank_id,len(self.functor_list)-1),
                    (len(self.functor_list)-1,highlight_rank_id),
                ])
                # 互换索引(把要删除的点与最后一点换位)
                map_rank = lambda rank: switch_rank_dict.get(rank, rank) 
                # vertical
                # 互换
                # 删除最后一个
                self.functor_list = [
                    self.functor_list[map_rank(rank)]
                    for rank, functor in enumerate(self.functor_list)
                ][:-1]
                # edge delete
                # 把当前点和最后一个点互换
                # 然后删除最后一个点, 这样就没有移位的问题
                new_link_table = self.link_table
                print('highlight_rank_id', highlight_rank_id)
                print('new_link_table.raw', new_link_table)
                # 互换
                new_link_table = dict(
                    (map_rank(from_rank), [
                        map_rank(to_rank) 
                        for to_rank in to_rank_list
                    ])
                    for from_rank, to_rank_list in new_link_table.items()
                )
                print('new_link_table.switch', new_link_table)
                # 删除
                new_link_table = dict(
                    (from_rank, [
                        to_rank 
                        for to_rank in to_rank_list
                        if to_rank != len(self.functor_list)
                    ])
                    for from_rank, to_rank_list in new_link_table.items()
                    if from_rank != len(self.functor_list)
                )
                print('new_link_table.del', new_link_table)
                self.link_table = new_link_table

            # self.functor_list = [
            #     functor 
            #     for functor in self.functor_list
            #     if functor.highlight != True
            # ]

        def render_genus(self, genus_name):
            self.functor_list.extend([
                Com.Com_Functor(self, 
                    **functor_param
                )
                for functor_param in genus_functors_param(genus_name)
            ])

        def set_link_bind(self):
            if self.link_flag != 1:
                self.link_flag = 1
            else:
                self.cancel_link_flag()    
        def set_link_unbind(self):
            if self.link_flag != 2:
                self.link_flag = 2
            else:
                self.cancel_link_flag()    
        def cancel_link_flag(self, **kwargs):
            self.link_flag = 0            
            

        @classmethod
        def compo_js(cls_):
            class_name = cls_.__name__
    # var compose_data_to_cls = (functor)=><Auto_type {{...functor}}></Auto_type>
    #             (functor_list)=>{{
    #     console.log('.js.73 functor_list', functor_list)
    #     return functor_list.map(
    #         (functor)=><Auto_type {{...functor}}></Auto_type>
    #     )
    # }}
        # compose_data_to_cls={{compose_data_to_cls}}
        #common_act={{self.common_act}}
            return f"""
function {class_name}(self){{
    return <Canvas2.view {{...self}} />
}}
            """.strip()
    

    @module_info.registry_terminator
    class Com_Functor_map(Com_common):
        '对canvas的demo做一个封装'
        @staticmethod
        def m(): return dict(
            e_list=list
        )
        def init(self, cls_name=cls_default):
            self.cls_name = cls_name

        @classmethod
        def compo_js(cls_):
            class_name = cls_.__name__
            return f"""
function {class_name}(self){{
    return <Canvas.view/>
}}
            """.strip()
    

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
                e.common_act = self.common_act
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
                e.common_act = self.common_act
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
                            e.common_act = self.common_act
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
        self.common_act.call({{
            "idx":self.idx,
            "method":"onClick",
            "params":{{}}
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
            self.common_act.call({{
                "idx":self.idx,
                "method":"onEnter",
                "params":{{"text":text}}
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
            self.common_act.call({{
                "idx":self.idx,
                "method":"onEnter",
                "params":{{"text":text}}
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




