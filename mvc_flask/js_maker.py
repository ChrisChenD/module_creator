#!/usr/bin/env python3

from mvc_flask.module.mvc_plan import Plan, module_info

mvc_plan_dir = '/home/ubuntu/git/npm_pro/pages/mvc_plan'

# 自动解析 list 里面的html类
# swtch_case
def Auto_type(cls_list, compo_list):
    cls_case_list = [
        f"""
    if (data.cls_type_=='{cls.__name__}')
        return <{cls.__name__}.view {{...data}} ></{cls.__name__}.view>    
        """.rstrip()
        for cls in cls_list
    ]
    compo_case_list = [
        f"""
    if (data.cls_type_=='{cls.__name__}')
        return <{cls.__name__} {{...data}} ></{cls.__name__}>    
        """.rstrip()
        for cls in compo_list
    ]
    ret = f"""
    console.log('Error!: undifined type:', data)
    return <p>undefined type [{{data}}]</p>
    """.rstrip()
    # cls_case_list.append(f"""
    # console.log('Error!: undifined type:', data)
    # return <p>undefined type [{{data}}]</p>
    # """.rstrip())
    cls_case_list = '\n'.join(compo_case_list+cls_case_list+[ret,])
    return f"""
export function Auto_type(data){{
    {cls_case_list}
}}
    """.strip()


js_module = [
    # class swtch_case code
    # for list parse
    Auto_type(module_info.cls_list, module_info.compo_list),
    # compo code
    '\n'.join([compo.compo_js() for compo in module_info.compo_list]),
    
]
# for obj in Plan.default_module().traverse():
for class_ in module_info.cls_list:
    obj = class_(None)
    js_module.append(obj.js_code())
    print(obj.js_code())

with open(f'{mvc_plan_dir}/libs/module.js', 'w+') as f:
    f.write('\n'.join(js_module))


