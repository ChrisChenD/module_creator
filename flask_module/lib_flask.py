#!/usr/bin/env python3

import json
from flask import Flask,jsonify,request
# import requests
# from flask_module.string_to_table import string_to_table, data_module

#create the object of Flask
app  = Flask(__name__)


#created home view
class Flask_url:
    obj = None
    prefix = ''
    # dynamic = ['db_name', 'table_name']
    dynamic = []
    @classmethod
    def registry(cls, app):
        path = "/".join(['', cls.prefix, cls.__name__, 
            *[f"<{var}>" for var in cls.dynamic]
        ])
        f_name = '_'.join(['', cls.prefix, cls.__name__])
        def delivery(*args, **kwargs):
            return Flask_url.delivery(cls, *args, **kwargs)
        delivery.__name__ = f_name
        print('regi', delivery.__name__, path)
        # @app.route(f'/home', methods=['GET', 'POST'])
        f = app.route(path, methods=['GET', 'POST'])
        cls.delivery = f(delivery)
        cls.obj = cls()
    # @classmethod
    def delivery(cls, *args, **kwargs):# sub class
        self = cls.obj
        if request.method == 'GET':
            return self.get(*args, **kwargs)
        if request.method == 'POST':
            return self.post(json.loads(request.data), *args, **kwargs)
        print('delivery::: method error!', request.method)

    def get(self):
        return self.render()
    def post(self, params):
        self.params = params
        return self.render()
    def render(self):
        return 'render default'