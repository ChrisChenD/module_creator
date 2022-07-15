#!/usr/bin/env python3
from flask_module.panda_code import Panda_code
def add_tab(s, tab_n):
    line_move = lambda line: ' '*4*tab_n + line
    if tab_n < 0:
        line_move = lambda line: line[tab_n*4:]
    return '\n'.join([
        line_move(line)
        for line in s.split('\n')])

# 不同的Code_maker 决定不同平台的code如何生成
# 默认是panda_code
class Code_maker:
    def __init__(self, plan):
        self.plan = plan
    
    @property
    def code(self):
        print('plan', self.plan)
        functor_list = self.plan['functor_list']
        print('functor_list:', len(functor_list))
        f_fellows = [f"f{i}" for i in range(len(functor_list)-1) if i>0]
        functor_list = '\n'.join([
            Panda_code(functor, i).code
            for i,functor in enumerate(functor_list)
        ])
        r = f"""
#!/usr/bin/env python3
import pandas 
{Panda_code.import_libs()}

{functor_list}

dfs = []
for i, chunk in enumerate(f_root()):
    for proc in {f_fellows}:
        chunk = proc(chunk)
    dfs.append(chunk)
    if i >= 2:
        break
df = pandas.concat(dfs, axis=0)
f_save(df)
# ok!
# file = "task/out2_1.xlsx"
# print('write', file)
# with pandas.ExcelWriter(file) as writer:
#     # hp1.add_sheet(writer)
#     df.to_excel(writer, sheet_name='商机明细表-常量表', index=False)
        """.strip()
        
        return "\n".join([r, f'# {str(self.plan)}', ])# r + str(self.plan)
