
from math import fabs
from module.module_base import Module_base, module_info, cls_default
from module.compo.compo_html import Com_html,Com_common
from plan_flask.module.functor.functor import pandas_king


class Com_functor(Com_html):
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
            functor_type=str,
        )
        # def init(self, x, y, name, functor_idx, cls_name=cls_default):
        def init(self, x, y, name, spec_id, cls_name=cls_default):
            self.x, self.y = x, y
            self.name = name
            self.spec_id = spec_id# 每种算子一个唯一id
            self.functor_type = 'leaf'
            self.highlight = False
            self.select = False
            self.cls_name = cls_name
            self.config_param = dict()# 算子的自己
            # self.onMousedown_recall = onMousedown
        def f_id(self):
            for i,functor in enumerate(self.root.canvas.functor_list):
                if functor.idx == self.idx:
                    return i

        @property
        def cur_functor(self):
            return pandas_king.cur_functor(self)
        def set_plan_cur_functor(self):
            # plan = self.root
            # input_name_list = self.root.canvas.get_input_name_list(self.f_id())
            self.root.cur_functor.init(
                self.cur_functor.config_compose_list
                # output_list = self.functor_output(),
            )


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
            '表单compose js'
            return self.cur_functor.compose_list
            #     self.functor_idx, self, 
            #     input_name_list=input_name_list    
            # )

        def code(self, f_id):
            # return pandas_king.functor_code(self.functor_idx, f_id)
            return self.cur_functor.code
        
            
        @classmethod
        def compo_js(cls_):
            class_name = cls_.__name__
            return f"""
function {class_name}(self){{
    return <Functor2.view {{...self}}/>
}}
            """.strip()
    
            
