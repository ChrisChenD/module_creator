#!/usr/bin/env python3

from flask import Flask,jsonify,request
app = Flask(__name__)

from flask_module.string_to_table import string_to_table
import requests

@app.route('/')
def hello_flask():
   return 'Flask'

@app.route('/hello')
def hello_world():
   return 'flask: [Hello]'

@app.route('/json_test')
def hello_json():
   return jsonify(dict(name='jname', value=['json_test']))


@app.route('/table/<table_string>')
def get_product(table_string):
   return jsonify(string_to_table(table_string))



# @app.route('/next')
# def get_product(table_string):
#    return string_to_table(table_string)


if __name__ == '__main__':
   app.run()

