from module.module_base import Module_base, module_info, cls_default
from module.compo.compo_functor import Com_functor,Com_common
from plan_flask.module.functor.functor import pandas_king


class Functor_graph:
    def __init__(self):
        self.graph_functor_list=[]
        self.graph_link_table={}
        # idx
    def adj(self, f_id):
        return self.graph_link_table[f_id]
    
    def adj_reverse(self, f_id):
        r = []
        for from_id, to_id_list in self.graph_link_table.items():
            if f_id in to_id_list:
                r.append(from_id)
        return r

    def set_functor_list(self, new_functor_list):
        self.graph_functor_list = new_functor_list
        self.graph_link_table={}
    
    def add_e(self, from_id, to_id):
        if from_id not in self.graph_link_table:
            self.graph_link_table[from_id] = []
        if to_id not in self.graph_link_table[from_id]:
            self.graph_link_table[from_id].append(to_id)
    def add_v(self, functor):
        self.graph_functor_list.append(functor)
    def swap_v(self, from_i, to_i):
        self.graph_functor_list[from_i],self.graph_functor_list[to_i]=self.graph_functor_list[to_i],self.graph_functor_list[from_i]
        self.swap_e(from_i, to_i)
    def swap_e(self, from_i, to_i):
        print('swap_e', from_i, to_i)
        swap_dict = {from_i:to_i, to_i:from_i}
        swap_value = lambda v:swap_dict.get(v, v)
        print('swap_value', swap_value(from_i), swap_value(to_i))
        print('swap_dict', swap_dict)

        self.graph_link_table = dict(
            (swap_value(from_i), [
                swap_value(to_i)
                for to_i in to_i_list
            ])
            for from_i, to_i_list in self.graph_link_table.items()
        )

    def del_e(self, from_id, to_id):
        if from_id not in self.graph_link_table:
            return 
        self.graph_link_table[from_id] = [
            idx
            for idx in self.graph_link_table
            if idx != to_id 
        ]
    def del_v(self, idx):
        max_idx = len(self.graph_functor_list)-1
        # print('idx', idx)
        # print('max_idx', max_idx)
        # print('raw:self.graph_link_table', self.graph_link_table)
        self.swap_v(idx, max_idx)
        # self.swap_e(idx, max_idx)
        # print('swap:self.graph_link_table', self.graph_link_table)
        # del max_idx
        self.graph_functor_list = self.graph_functor_list[:-1]
        # del v
        self.graph_link_table = dict(
            (from_i, [
                to_i
                for to_i in to_i_list
                if to_i != max_idx
            ])
            for from_i, to_i_list in self.graph_link_table.items()
            if from_i != max_idx
        )

Functor_class = Com_functor.Com_Functor


class Com_canvas(Com_functor):
    @module_info.registry_terminator
    # class Com_Canvas(Com_common, Functor_graph):
    # class Com_Graph(Com_common, Functor_graph, Functor_class):
    class Com_Graph(Com_functor.Com_Functor, Functor_graph):
    # class Com_Graph(Com_common, Functor_graph):
        'canvas简单版本'
        def __init__(self, father, *args, **kwargs):
            Com_functor.Com_Functor.__init__(self, father, *args, **kwargs)
        @staticmethod
        def m(): return dict(
            # graph_w=int,
            # graph_h=int,
            # graph_level=int,
            # head=Com_functor.Com_Functor,
            graph_functor_list=list,
            graph_link_table=list,
            graph_link_flag=bool,
            **Com_functor.Com_Functor.m()
        )
        graph_base_wh = 800, 500 
        # @classmethod
        # def graph_level_wh(cls_, functor_level):
        #     w, h = 800, 500 
        #     if functor_level == cls_.levelFunctor:
        #         w,h = w/5,h/5
        #     if functor_level == cls_.levelSubFunctor:
        #         w,h = w/5,h/5
        #     if functor_level == cls_.levelUnseen:
        #         w,h = 0,0
        #     return w,h            
                

        # def init(self, x, y, name, 
        #     offset_xy, 
        #     functor_level, functor_list, link_table, 
        #     cls_name=cls_default,
        #     **kwargs,
        #     ):
        def init(self, spec_id, name, offset, level,
            graph_functor_list,
            graph_link_table,
            # graph_link_flag,
            cls_name=cls_default,
            **kwargs):
            # spec_id = pandas_king.make_spec_id('module', 'custom')
            Com_functor.Com_Functor.init(self,
                spec_id, name, offset, level,
                cls_name=cls_name
            )
            self.graph_functor_list = graph_functor_list
            self.graph_link_table = graph_link_table
            self.graph_link_flag = 0
            
        # def CODE_GENERATE(self):
        #     code = [
        #         functor.code(f_id)
        #         for f_id,functor in enumerate(self.graph_functor_list)
        #     ]
        #     code = '\n'.join(code)
        #     self.call_param_func(
        #         # self.root.op.idx,
        #         self.root.idx,
        #         'SET_CODE',
        #         dict(code=code)
        #     )
        
        def add_link(self, from_rank, to_rank):
            if self.graph_link_flag == 1:
                self.link_bind(from_rank, to_rank)
            if self.graph_link_flag == 2:
                self.link_unbind(from_rank, to_rank)
        def link_bind(self, from_rank, to_rank):
            self.add_e(from_rank, to_rank)
            self.cancel_link_flag()
            
        def link_unbind(self, from_rank, to_rank):
            self.del_e(from_rank, to_rank)
            self.cancel_link_flag()

        def get_functor(self, idx):
            for functor in self.graph_functor_list:
                if functor.idx == idx:
                    return functor
        
        def dehighlight_functor(self):
            '反高亮'
            for functor in self.graph_functor_list:
                functor.highlight = False
        def highlight_functor(self, functor_idx):
            '高亮/选中functor'
            functor = self.get_functor(functor_idx)
            functor.highlight = True
            self.highlight_functor_show_in_plan()
        
        def highlight_functor_show_in_plan(self):
            functor, f_id = None,None
            for i,f in enumerate(self.graph_functor_list):
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
                self.graph_functor_list[input_id].name
                for input_id in input_id_list
            ]
            return input_name_list
        
        def select_functor(self, functor_idx):
            '对象被点击选中, 用来拖拽, 重定位判定'
            functor = self.get_functor(functor_idx)
            functor.select = True
        def cancel_select_functor(self):
            '取消选中'
            for functor in self.graph_functor_list:
                functor.select = False
        def move_functor_to(self, idx, x, y):
            functor = self.get_functor(idx)
            # functor.x, functor.y = x, y
            functor.offset = dict(
                x=x,y=y
            )
        
        def functor_rank_from_idx(self, idx):
            for rank,functor in enumerate(self.graph_functor_list):
                if functor.idx == idx:
                    return rank
            return None

        def onMousedownSub(self, idx):
            '当link的时候传来连接两个functor的消息'
            assert self.graph_link_flag != 0
            # 找到高亮算子, 被对方连接
            rank = self.functor_rank_from_idx(idx)
            from_rank = None
            for rank_i, functor in enumerate(self.graph_functor_list):
                if functor.highlight == True:
                    from_rank = rank_i
            # 必须有高亮算子才可以连接
            assert rank is not None
            assert from_rank is not None
            self.add_link(from_rank, rank)
        
        def onMouseupSub(self, idx, x, y):
            print('onMouseup', 207)
            # self.dehighlight_functor()
            # self.cancel_select_functor()
            self.move_functor_to(idx, x, y)
            self.dehighlight_functor()
            self.highlight_functor(idx)

        # def add_functor(self, kwargs):
        #     self.graph_functor_list.append(
        #         Com_canvas.Com_Functor(self, **kwargs)
        #     )
        
        def del_highlight_functor(self):
            '图删除点, 需要连带删除边'
            highlight_rank_id = None
            for rank, functor in enumerate(self.graph_functor_list):
                if functor.highlight:
                    highlight_rank_id = rank
                    break
            if highlight_rank_id is not None:
                self.del_v(highlight_rank_id)
                
        def render_genus(self, genus_name):
            print('len(self.graph_functor_list)', len(self.graph_functor_list))
            self.graph_functor_list.extend([
                getattr(Com_canvas, functor_param['functor_cls'])(
                    self, **functor_param
                )
                # Com_canvas.Com_Functor(self,
                #     **functor_param
                # )
                for functor_param in pandas_king.render_genus_dict(genus_name)
            ])
            print('len(self.graph_functor_list)', len(self.graph_functor_list))

        def set_link_bind(self):
            if self.graph_link_flag != 1:
                self.graph_link_flag = 1
            else:
                self.cancel_link_flag()

        def set_link_unbind(self):
            if self.graph_link_flag != 2:
                self.graph_link_flag = 2
            else:
                self.cancel_link_flag()    
        def cancel_link_flag(self, **kwargs):
            self.graph_link_flag = 0

        @classmethod
        def compo_js(cls_):
            class_name = cls_.__name__
            return f"""
function {class_name}(self){{
    return <Canvas2.view {{...self}} />
}}
            """.strip()


