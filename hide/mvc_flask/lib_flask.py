#!/usr/bin/env python3

import json,copy
from flask import Flask,jsonify,request
import threading

app  = Flask(__name__)

#created home view
class Flask_url:
    obj = None
    prefix = ''
    # dynamic = ['db_name', 'table_name']
    dynamic = []
    mutex = threading.Lock()
    def __init__(self):
        self.params = dict()
        self.init()
    def init(self): pass

    @property
    def data(self): 
        'read/write lock'
        self.mutex.acquire()
        params = copy.deepcopy(self.params)
        self.mutex.release()
        return params
    @data.setter
    def data(self, new_params): 
        self.mutex.acquire()
        self.params = copy.deepcopy(new_params)
        self.mutex.release()
    def set(self, key, value):
        'set params: params[key]=value'
        self.mutex.acquire()
        self.params[key] = value
        self.mutex.release()

    @classmethod
    def registry(cls, app):
        path = "/".join(['', cls.prefix, cls.__name__, 
            *[f"<{var}>" for var in cls.dynamic]
        ])
        f_name = '_'.join(['', cls.prefix, cls.__name__])
        def delivery(*args, **kwargs):
            return Flask_url.delivery(cls, *args, **kwargs)
        delivery.__name__ = f_name
        # @app.route(f'/home', methods=['GET', 'POST'])
        f = app.route(path, methods=['GET', 'POST'])
        cls.delivery = f(delivery)
        cls.obj = cls()
    # @classmethod
    def delivery(cls, **dynamic_kwargs):# sub class
        self = cls.obj
        if request.method == 'GET':
            dynamic_kwargs = dict(
                (k,v) for k,v in
                dynamic_kwargs.items()
                if v is not None)
            if len(dynamic_kwargs) != len(self.dynamic):# 前端空值
                return None
            return self.get(**dynamic_kwargs)
        if request.method == 'POST':
            return self.post(json.loads(request.data), **dynamic_kwargs)
        print('delivery::: method error!', request.method)

    def get(self):
        return self.render()
    def post(self, params):
        self.params = params
        return self.render()
    def render(self):
        return 'render default'

        



