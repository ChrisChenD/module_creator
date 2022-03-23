#!/usr/bin/env python3

import json
from flask import Flask,jsonify,request
# import requests
# from flask_module.string_to_table import string_to_table, data_module

#create the object of Flask
app  = Flask(__name__)


#created home view
class Flask_class:
    obj = None
    prefix = ''
    @classmethod
    # def registry(cls, f, pre_path=''):
    def registry(cls, app):
        # f = 
        # @app.route()
        #     , methods=['GET', 'POST'])
        path = "/".join(['', cls.prefix, cls.__name__])
        f_name = '_'.join(['', cls.prefix, cls.__name__])
        def delivery():
            return Flask_class.delivery(cls)
        delivery.__name__ = f_name
        print('regi', delivery.__name__)
        f = app.route(path, methods=['GET', 'POST'])
        # cls.delivery = f(cls.delivery)
        cls.delivery = f(delivery)
        cls.obj = cls()
    # @app.route(f'/home', methods=['GET', 'POST'])
    # @classmethod
    def delivery(cls):# sub class
        self = cls.obj
        if request.method == 'GET':
            return self.get()
        if request.method == 'POST':
            return self.post(json.loads(request.data))
    def get(self):
        return self.render()
    def post(self, params):
        self.params = params
        return self.render()