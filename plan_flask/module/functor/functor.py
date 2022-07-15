from module.compo.compo_html import Com_html,Com_common
# 引入算子
from module.functor.input_genus import *
from module.functor.output_genus import *

from module.functor.media_genus import *
from module.functor.evolution_genus import *
from module.functor.divide_genus import *
from module.functor.union_genus import *
from module.functor.module_genus import *
# media 中介
# evolution 演化
# divide 分裂
# union 聚合

# class Cur_functor:
#     def __init__(self, spec, canvas_config):
#         self.spec = spec
#         self.canvas_config = canvas_config
#     @property
#     def code(self):
#         cls_name = self.spec.name
#         return cls_name(self.canvas_config)



class Species_base:
    def __init__(self, cn, params=None):
        self.name = None
        self.cn = cn
        self.params = params
    def create_from_canvas_functor(self, canvas_functor):
        cls_name = self.name
        return eval(cls_name)(canvas_functor)

#     def compose_list(self, father, input_name_list):
#         if self.params is None:
#             return [
#                 Com_html.Com_Dict(father, e_dict=dict(
#                     functor_name=Com_html.Com_Button(father, self.cn, onClick=None),
#                     # input=Com_html.Com_Button(father, 'input', onClick=None),
#                     input=Com_html.Com_List(father, e_list=[
#                         Com_html.Com_Button(father, input_name, onClick=None)
#                         for input_name in input_name_list
#                     ]),
#                     output=Com_html.Com_Button(father, 'output', onClick=None),
#                     param_config=Com_html.Com_Button(father, 'param_config', onClick=None),
#                 ))
#             ]
#         return self.params.compose_list()

#     def code(self, f_id):
#         if self.params is None:
#             return f'''
# def f{f_id}_{self.name}():
#     '{self.cn}'
#     print('f{f_id}_{self.name} run!')
#     return None
# '''
#         return f'''
# def f{f_id}_{self.name}({self.param.input.code()}):
#     '{self.cn}'
#     return {self.param.output.code()}
# '''


class Genus_base:
    # def __init__(self, name, cn, sons):
    def __init__(self, cn, species_dict):
        # self.name = name
        self.cn = cn
        self.species_dict = species_dict
        for spec_name, spec in species_dict.items():
            spec.name = spec_name
    def __getitem__(self, Slice):
        return self.species_dict.__getitem__(Slice)


            
class Kingdom_base:
    def __init__(self, name, cn, genus_dict):
        self.name = name
        self.cn = cn
        self.genus_dict = genus_dict
        for genus_name, genus in genus_dict.items():
            genus.name = genus_name
    def __getitem__(self, Slice):
        return self.genus_dict.__getitem__(Slice)

    def render_genus_dict(self, genus_name):
        base_height = 50
        base_left = 100
        offset_left = 100
        # def genus_functors_param(genus_name):
        species_list = self.genus_dict[genus_name].species_dict.values()
        # species_list = [spe.name for spe in species_list]
        # species_table = genus_table[genus_name]
        def functor_param(idx, species):
            return dict(
                offset = dict(
                    x=base_left+idx*offset_left, 
                    y=base_height, 
                ),
                # 种 Species
                name=species.cn,
                spec_id=self.make_spec_id(genus_name, species.name),
                level=1,
                # functor_cls='Com_Functor',# 我们怎么区分不同类型的算子
                functor_cls=species.cls,# 我们怎么区分不同类型的算子
            )
        def graph_param(idx, species):
            d = functor_param(idx, species)
            d['graph_functor_list'] = []
            d['graph_link_table'] = {}
            return d
            
        r = [
            functor_param(idx,species) if species.cls=='Com_Functor' 
                else graph_param(idx,species)
            for idx,species in enumerate(species_list)
        ]
        print('r', r)
        return r
    def genus_name_list(self):
        return [(genus.name, genus.cn) for genus in self.genus_dict.values()]
    
    def make_spec_id(self, genus_name, spec_name):
        return '.'.join([genus_name, spec_name])
    
    def get_spec_by_spec_id(self, spec_id):
        genus_name, spec_name = spec_id.split('.')
        return self[genus_name][spec_name]
    def cur_functor(self, canvas_functor):
        spec_id = canvas_functor.spec_id
        spec = self.get_spec_by_spec_id(spec_id)
        return spec.create_from_canvas_functor(canvas_functor)
        
        
    # def functor_compose_list(self, functor_idx, compose_father, input_name_list):
    #     cur_functor = self.get_functor_by_idx(functor_idx)
    #     return cur_functor.compose_list(compose_father,
    #         input_name_list = input_name_list
    #     )
    
    # def functor_code(self, functor_idx, f_id):
    #     functor = self.get_functor_by_idx(functor_idx)
    #     return functor.code(f_id)
        
        

pandas_king = Kingdom_base(
    'pandas_king', '潘达斯', 
    genus_dict = dict(
        input=Genus_base(
            cn='输入',
            species_dict=dict(
                F_ReadMysql=F_ReadMysql(
                    cn='读 MYSQL'
                ),
                F_MysqlFindList=F_MysqlFindList(
                    cn='按名单查询 MYSQL'
                ),
            ),
        ),
        # '输出':{#(表 -> 数据库/文件)
        #     '保存到 EXCEL',
        # },
        output=Genus_base(
            cn='输出',
            species_dict=dict(
                F_SaveExcel=F_SaveExcel(
                    cn='保存到 EXCEL'
                ),
            ),
        ),
        # '演化':{#(表->表)(列->列)
        #     '表:列重命名',
        #     '表:分组统计',
        #     '表:条件过滤',
        # },
        evolution=Genus_base(
            cn='演化',
            species_dict=dict(
                F_TableColRename=F_TableColRename(
                    cn='表:列重命名'
                ),
                F_TableGroup=F_TableGroup(
                    cn='表:分组统计'
                ),
                F_TableRowFilter=F_TableRowFilter(
                    cn='表:条件过滤'
                ),
            ),
        ),
        # '中介':{#(表->列, 列->表)
        #     '名单转表',
        #     '表转名单',
        # },
        media=Genus_base(
            cn='中介',
            species_dict=dict(
                F_ListToTable=F_ListToTable(
                    cn='名单转表'
                ),
                F_TableToList=F_TableToList(
                    cn='表转名单'
                ),
            ),
        ),
        # '聚合':{#(多表->单表)
        #     '名单聚合',
        #     '表聚合',
        # },
        union=Genus_base(
            cn='聚合',
            species_dict=dict(
                F_ListUnion=F_ListUnion(
                    cn='名单聚合'
                ),
                F_TableUnion=F_TableUnion(
                    cn='表聚合'
                ),
            ),
        ),
        # '分裂':{#(单表->多表)
        #     '名单:条件分裂',
        #     '名单:分页分裂',
        #     '表:条件分裂',
        #     '表:分页分裂',
        # },
        divide=Genus_base(
            cn='分裂',
            species_dict=dict(
                F_ListCasePartition=F_ListCasePartition(
                    cn='名单:条件分裂'
                ),
                F_ListPagePartition=F_ListPagePartition(
                    cn='名单:分页分裂'
                ),
                F_TableCasePartition=F_TableCasePartition(
                    cn='表:条件分裂'
                ),
                F_TablePagePartition=F_TablePagePartition(
                    cn='表:分页分裂'
                ),
            ),
        ),
        module=Genus_base(
            cn='模块',
            species_dict=dict(
                F_CustomModule=F_CustomModule(
                    cn='自定义模块',
                    cls='Com_Graph',# Com_Functor
                ),
            ),
        ),
    )
)


