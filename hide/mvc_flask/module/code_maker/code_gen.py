from mvc_flask.module.code_maker.panda_functor import panda_functor

def import_libs():
    return f"""
import pandas
from pandaUtil_mysql_chain import mysql_chain
from pandaUtil_append import chunk_append,readMysql
        """.strip()

def code_gen(functor_list):
    print('functor_list', functor_list)
    
    f_fellows = [f"f{i}" for i in range(len(functor_list)-1) if i>0]
    functor_def_list = '\n'.join([
        getattr(panda_functor, functor.__class__.__name__)(
            functor_id, 
            *functor.param_for_code(),
        )
        for functor,functor_id in enumerate(functor_list)
    ])
    code = f"""
#!/usr/bin/env python3
{import_libs()}

{functor_def_list}

if __name__ == '__main__':
    dfs = []
    for i, chunk in enumerate(f_root()):
        for proc in {f_fellows}:
            chunk = proc(chunk)
        dfs.append(chunk)
        if i >= 2:
            break
    df = pandas.concat(dfs, axis=0)
    f_save(df)
        """.strip()
        
        # return "\n".join([r, f'# {str(self.plan)}', ])# r + str(self.plan)
    return code

    
    
    
    return f"""{('functor_list', functor_list)}
    code gen
    CODE_GENERATE!!!!
    """

