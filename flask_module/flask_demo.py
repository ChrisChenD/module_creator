#!/usr/bin/env python3

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
   table = data_module.get_table(db_name, tb_name)
   print('table_info:', table)
   cols = [dict(
      name=col['name'],
      cname=col['cname'] if len(col['cname'])<10 else col['cname'][:10]+' ...',
      type=col['type']
      )
      for col in table['cols']
   ]
   return jsonify(dict(
      tb_name=table['table_name'],
      tb_cname = table['table_cn'],
      cols=cols,
      samples=table['data']
   ))


# @app.route('/next')
# def get_product(table_string):
#    return string_to_table(table_string)


if __name__ == '__main__':
   app.run()

