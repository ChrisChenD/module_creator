#!/usr/bin/env python3

from mvc_flask.module.mvc_plan import Plan, module_info

mvc_plan_dir = '/home/ubuntu/git/npm_pro/pages/mvc_plan'


def Auto_type(cls_list):
    cls_case_list = [
        f"""
    if (data.cls_type_=='{cls.__name__}')
        return <{cls.__name__}.view {{...data}}></{cls.__name__}.view>    
        """.rstrip()
        for cls in cls_list
    ]
    cls_case_list.append(f"""
    return <p>undefined type [{{data}}]</p>
    """.rstrip())
    cls_case_list = '\n'.join(cls_case_list)
    return f"""
export function Auto_type(data){{
    {cls_case_list}
}}
    """.strip()


js_module = [
    Auto_type(module_info.cls_list)
]
# for obj in Plan.default_module().traverse():
for class_ in module_info.cls_list:
    obj = class_(None)
    js_module.append(obj.js_code())
    print(obj.js_code())

with open(f'{mvc_plan_dir}/libs/module.js', 'w+') as f:
    f.write('\n'.join(js_module))




# for obj in module.traverse_module():
#     print(obj.js_code())



# print('module', module)
# print('module.functor_list', module.functor_list)
# print('module.new_functor_list', module.new_functor_list)

'''
export PYTHONPATH=`pwd`;python mvc_flask/js_maker.py

'''