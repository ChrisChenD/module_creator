#!/usr/bin/env python3

from csv import excel
from flask import jsonify,request
from lib_flask import app, Flask_url

import copy
from plan_flask.module.mvc_plan import Plan

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
        return self.get(plan_name)
        
        # return 'call!'
        # module = self.data[plan_name]
        # return module.to_json_dict()
        # return new_module.to_json_dict()

# class new_framework(Flask_url):
#     dynamic = ['frame_name']
#     def get(self, frame_name):
#         return {
#             'name': frame_name
#         }
#     def post(self, call_param, frame_name):
#         print('POST: param:', call_param)


if __name__ == "__main__":
    
    plan.registry(app)
    # new_framework.registry(app)
    app.run(debug=True)

    """
export PYTHONPATH=`pwd`;python plan_flask/app.py

export PYTHONPATH=`pwd`;python plan_flask/js_maker.py;python plan_flask/app.py;

http://175.27.223.106:3000/plan/t1


ssh ubuntu@175.27.223.106
"""

# xx 

