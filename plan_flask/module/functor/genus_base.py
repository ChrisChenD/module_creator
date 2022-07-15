from module.compo.compo_html import Com_html,Com_common


class Functor_base:
# class Species_base:
    def __init__(self, cn, canvas_functor=None, cls='Com_Functor'):
        self.cn = cn
        self.canvas_functor = canvas_functor
        self.cls = cls
        # self.params = params
    def create_from_canvas_functor(self, canvas_functor):
        return self.__class__(
            self.cn,
            canvas_functor = canvas_functor
        )
    @property
    def config_compose_list(self):
        father = self.canvas_functor
        input_name_list = father.root.canvas.get_input_name_list(father.f_id())
        # input_name_list = father.get_input_name_list()
        return [
            Com_html.Com_Dict(father, e_dict=dict(
                functor_name=Com_html.Com_Button(father, self.cn, onClick=None),
                # input=Com_html.Com_Button(father, 'input', onClick=None),
                input=Com_html.Com_List(father, e_list=[
                    Com_html.Com_Button(father, input_name, onClick=None)
                    for input_name in input_name_list
                ]),
                output=Com_html.Com_Button(father, 'output', onClick=None),
                param_config=Com_html.Com_Button(father, 'param_config', onClick=None),
            ))
        ]
    @property
    def code(self):
        f_id = self.canvas_functor.f_id()
        f_name = self.__class__.__name__
        return f'''
def f{f_id}_{f_name}():
    '{self.cn}'
    print('f{f_id}_{f_name} run!')
    return None
'''

