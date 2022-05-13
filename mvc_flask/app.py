#!/usr/bin/env python3

from csv import excel
from flask import jsonify,request
from lib_flask import app, Flask_url

import copy
from mvc_flask.module.mvc_plan import Plan


class plan(Flask_url):
    dynamic = ['plan_name']
    # plan = get(plan_name, default_plan_maker())
    # set(plan_name, plan)
    def init(self):
        pass
    def get(self, plan_name):
        if plan_name not in self.data:
            print('plan_name', plan_name, 'not find: set default')
            self.set(plan_name, Plan.default_module(plan_name))
        
        module = self.data[plan_name]
        return module.to_json_dict()
    def post(self, call_param, plan_name):
        module = self.data[plan_name]

        new_module = module.call(call_param)
        self.set(plan_name, new_module)
        return 'call!'



if __name__ == "__main__":
    
    plan.registry(app)
    app.run(debug=True)


    """
export PYTHONPATH=`pwd`;python mvc_flask/app.py

export PYTHONPATH=`pwd`;python mvc_flask/js_maker.py;python mvc_flask/app.py;

http://109.244.159.137:3000/mvc_plan/t1
"""



