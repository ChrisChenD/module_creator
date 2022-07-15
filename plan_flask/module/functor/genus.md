#!/usr/bin/env python3
# from module.compo import Com, Module_base_debug
from module.functor.genus import pandas_king

"""
界 Kingdom
门 Phylum
亚门 Subphylum
总纲 Superclass
纲 Class
亚纲 Subclass
总目 Superoder
目 Order
亚目 Suborder
总科 Superfamily
科 Family
亚科 Subfamily
属 Genus
亚属 Subgenus
种 Species
"""
"""
算子分类学:

我们采用 几个级别进行命名:
种 Species
    算子名字
属 Genus
    输入算子(数据库/文件 -> 表)
    输出算子(表 -> 数据库/文件)
    演化算子(表->表)
    聚合算子(多表->单表)
    分裂算子(单表->多表)
科 Family
    基本算子
    复合算子
        多个基本算子的合成算子
界 Kingdom
    算子属于哪个计算平台
"""
"""
参数分类学:
名称/字符串/数字()
列表
提示框.选择
提示框.文本输入
提示框.提示.只读.
"""
# base_height = 50
# base_left = 100
# offset_left = 100
# # Genus
# genus_table = {
#     '输入':{#(数据库/文件 -> 表)
#         '读 MYSQL',
#         # 'ReadMYSQL',
#         # 'READMYSQLAAAAAAAAAAAAAAAAAAA',# test ALPHA
#         # 'readmysqlaaaaaaaaaaaaaaaaaazzzzz',# test alpha
#         # '444444444444444444444',# test digit
#         # '按名单按名单按名单按名单按名单按名单按名单按名单',# test chinese
#         '按名单查询 MYSQL',
#     },
#     '输出':{#(表 -> 数据库/文件)
#         '保存到 EXCEL',
#     },
#     '演化':{#(表->表)(列->列)
#         '表:列重命名',
#         '表:分组统计',
#         '表:条件过滤',
#     },
#     '中介':{#(表->列, 列->表)
#         '名单转表',
#         '表转名单',
#     },
#     '聚合':{#(多表->单表)
#         '名单聚合',
#         '表聚合',
#     },
#     '分裂':{#(单表->多表)
#         '名单:条件分裂',
#         '名单:分页分裂',
#         '表:条件分裂',
#         '表:分页分裂',
#     },
# }

# def genus_button_params(father):
#     # genus_line.init(father, 
#     return [
#         dict(father=father,  
#             value=genus_name, 
#             onClick=[
#                 father.root.canvas.idx,
#                 'render_genus',
#                 dict(genus_name=genus_name)
#             ],
#         )
#         for idx, (genus_name, species_table) in enumerate(genus_table.items())
#         # 属 Genus
#     ]
#     # )
#     # return genus_line

# # x=idx*80, y=base_height, 

# # render_genus

# def genus_functors_param(genus_name):
#     species_table = genus_table[genus_name]
    
#     return [
#         dict(
#             x=base_left+idx*offset_left, y=base_height, 
#             # 种 Species
#             name=species_name
#         )
#         for idx,species_name in enumerate(species_table)
#     ]






