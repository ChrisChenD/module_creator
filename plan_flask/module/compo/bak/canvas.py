from module.module_base import Module_base, module_info, cls_default
from module.compo.compo_functor import Com_functor,Com_common
from plan_flask.module.functor.functor import pandas_king

class Functor_graph:
    def __init__(self):
        self.functor_list=[]
        self.link_table={}
        # idx
    def adj(self, f_id):
        return self.link_table[f_id]
    
    def adj_reverse(self, f_id):
        r = []
        for from_id, to_id_list in self.link_table.items():
            if f_id in to_id_list:
                r.append(from_id)
        return r

    def set_functor_list(self, new_functor_list):
        self.functor_list = new_functor_list
        self.link_table={}
    
    def add_e(self, from_id, to_id):
        if from_id not in self.link_table:
            self.link_table[from_id] = []
        if to_id not in self.link_table[from_id]:
            self.link_table[from_id].append(to_id)
    def add_v(self, functor):
        self.functor_list.append(functor)
    def swap_v(self, from_i, to_i):
        self.functor_list[from_i],self.functor_list[to_i]=self.functor_list[to_i],self.functor_list[from_i]
        self.swap_e(from_i, to_i)
    def swap_e(self, from_i, to_i):
        print('swap_e', from_i, to_i)
        swap_dict = {from_i:to_i, to_i:from_i}
        swap_value = lambda v:swap_dict.get(v, v)
        print('swap_value', swap_value(from_i), swap_value(to_i))
        print('swap_dict', swap_dict)

        self.link_table = dict(
            (swap_value(from_i), [
                swap_value(to_i)
                for to_i in to_i_list
            ])
            for from_i, to_i_list in self.link_table.items()
        )

    def del_e(self, from_id, to_id):
        if from_id not in self.link_table:
            return 
        self.link_table[from_id] = [
            idx
            for idx in self.link_table
            if idx != to_id 
        ]
    def del_v(self, idx):
        max_idx = len(self.functor_list)-1
        # print('idx', idx)
        # print('max_idx', max_idx)
        # print('raw:self.link_table', self.link_table)
        self.swap_v(idx, max_idx)
        # self.swap_e(idx, max_idx)
        # print('swap:self.link_table', self.link_table)
        # del max_idx
        self.functor_list = self.functor_list[:-1]
        # del v
        self.link_table = dict(
            (from_i, [
                to_i
                for to_i in to_i_list
                if to_i != max_idx
            ])
            for from_i, to_i_list in self.link_table.items()
            if from_i != max_idx
        )



class Com_canvas(Com_functor):
    @module_info.registry_terminator
    class Com_Module(Com_common, Functor_graph):
        @staticmethod
        def m(): return dict(
            functor=Com_canvas.Com_Functor,
            graph=Com_canvas.Com_Graph,
        )
    # def init(self, w, h, functor_list, link_table, cls_name=cls_default):
    # def init(self, functor_params, graph_params, cls_name=cls_default):
    def init(self, module_name, w, h, functor_list, link_table, cls_name=cls_default):
        self.functor.init(x, y, module_name, spec_id)
        self.graph.init(w, h, functor_list, link_table)
        # self.w, self.h = w, h
        # self.functor_list = functor_list
        # self.link_table = link_table
        # self.link_flag = 0
        # self.cls_name = cls_name
        
    @module_info.registry_terminator
    # class Com_Canvas(Com_common, Functor_graph):
    class Com_Graph(Com_common, Functor_graph):
        'canvas简单版本'
        def __init__(self, father, *args, **kwargs):
            Com_common.__init__(self, father, *args, **kwargs)
        @staticmethod
        def m(): return dict(
            x=int,
            y=int,
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
        def CODE_GENERATE(self):
            code = [
                functor.code(f_id)
                for f_id,functor in enumerate(self.functor_list)
            ]
            code = '\n'.join(code)
            self.call_param_func(
                # self.root.op.idx,
                self.root.idx,
                'SET_CODE',
                dict(code=code)
            )
        
        def add_link(self, from_rank, to_rank):
            if self.link_flag == 1:
                self.link_bind(from_rank, to_rank)
            if self.link_flag == 2:
                self.link_unbind(from_rank, to_rank)
        def link_bind(self, from_rank, to_rank):
            self.add_e(from_rank, to_rank)
            self.cancel_link_flag()
            
        def link_unbind(self, from_rank, to_rank):
            self.del_e(from_rank, to_rank)
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
            functor, f_id = None,None
            for i,f in enumerate(self.functor_list):
                if f.highlight:
                    functor = f
                    f_id = i
            # plan = self.root
            # input_name_list = self.get_input_name_list(f_id)
            # plan.cur_functor.init(functor.config_compose_list(
            #     input_name_list = input_name_list,
            #     # output_list = self.functor_output(),
            # ))
            functor.set_plan_cur_functor()
        def get_input_name_list(self, f_id):
            input_id_list = self.adj_reverse(f_id)
            input_name_list = [
                self.functor_list[input_id].name
                for input_id in input_id_list
            ]
            return input_name_list
        
            
            
    
        def select_functor(self, functor_idx):
            '对象被点击选中, 用来拖拽, 重定位判定'
            functor = self.get_functor(functor_idx)
            functor.select = True
        def cancel_select_functor(self):
            '取消选中'
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
            # self.cancel_select_functor()
            self.move_functor_to(idx, x, y)
            self.dehighlight_functor()
            self.highlight_functor(idx)
            

        def add_functor(self, kwargs):
            self.functor_list.append(
                Com_canvas.Com_Functor(self, **kwargs)
            )
        def del_highlight_functor(self):
            '图删除点, 需要连带删除边'
            highlight_rank_id = None
            for rank, functor in enumerate(self.functor_list):
                if functor.highlight:
                    highlight_rank_id = rank
                    break
            if highlight_rank_id is not None:
                self.del_v(highlight_rank_id)
                
            
        def render_genus(self, genus_name):
            self.functor_list.extend([
                Com_canvas.Com_Functor(self,
                    **functor_param
                )
                for functor_param in pandas_king.render_genus_dict(genus_name)
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


