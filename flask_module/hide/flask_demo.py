#!/usr/bin/env python3

import json
from flask import Flask,jsonify,request
app = Flask(__name__)

from flask_module.string_to_table import string_to_table, data_module
import requests

@app.route('/')
def hello_flask():
    return 'Flask'

@app.route('/hello_text')
def hello_text():
    return 'flask-text: [Hello]'

@app.route('/hello_json')
def hello_json():
    return jsonify(dict(name='jname', value=['json_test']))

@app.route('/table_string/<table_string>')
def string_to_table(table_string):
    table_info = string_to_table(table_string)
    keys = table_info.keys()
    print(keys)
    return jsonify(table_info)

@app.route('/mysql')
def list_db():
   return jsonify(data_module.list_db())

@app.route('/mysql/<db_name>')
def list_table(db_name):
    return jsonify(data_module.list_table(db_name))

@app.route('/mysql/<db_name>/<tb_name>')
def get_table(db_name, tb_name):
    return jsonify(data_module.get_table(db_name, tb_name).info)
    

from task import Task
@app.route('/task/<task_name>')
def get_task(task_name):
    if task_name not in Task.registried:
        Task(task_name).registry()
     
    info = Task.registried[task_name].info
    print(f'task:{task_name}:')
    print(info)
    return jsonify(info)

@app.route('/task/<task_name>/<src_name>', methods=['GET','POST'])
def task_add_resource(task_name, src_name):
    task = Task.registried[task_name]
    if request.method == 'GET':
        return jsonify(task.get_src(src_name))
    if request.method == 'POST':
        task.set_src(src_name, request.get_json())

@app.route('/demo/table', methods=['GET','POST'])
def get_table_demo():
    from table_json import json_context
    
    return jsonify(json_context)

if __name__ == '__main__':
    app.run()