#!/usr/bin/env python3

from sys import prefix
from flask import jsonify,request
from lib_flask import app, Flask_class

from table_json import json_context

class home(Flask_class):
    def __init__(self):
        self.params = [1,2,3]
    def render(self):
        print('render!')
        return "<h1>codeloop.org, ID is {} </h1>".format(self.params)

class table(Flask_class):
    prefix = 'demo'
    def __init__(self):
        self.params = json_context
        self.params['name'] = 'table_info'
    # def get(self):
    #     # print('get select_list:', self.params['select_list'], self.params['name'])
    #     return super().get()
    def post(self, params):
        # print('post params:', params)
        print('post get select_list:', params['select_list'], self.params['name'])
        return super().post(params)
    def render(self):
        print('render:select_list: ', self.params['select_list'])
        return jsonify(self.params)

# home.registry(lambda f:f)

#run flask app
if __name__ == "__main__":
    home.registry(app)
    table.registry(app)
    app.run(debug=True)

    # r = home().get('abc')
    # print(r)

