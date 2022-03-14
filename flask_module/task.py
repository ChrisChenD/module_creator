#!/usr/bin/env python3
from flask_module.string_to_table import data_module

###

class Task:
    def __init__(self):
        self.desc = ""
        self.src_dict = dict()
        self.output = ''
    # def add_src(self):
    #     for key in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    #         if key not in dict():
    #             self.src_dict[key] = dict()
    #         return key
    def del_src(self, key):
        del self.src_dict[key]
    def get_src(self, key): 
        return self.src_dict[key]
    def set_src(self, key, value):
        self.src_dict[key] = value
    @property
    def src_info(self):
        return dict(
            (k, v['string'])
            for k,v in self.src_dict.items()
        )
    @property
    def info(self):
        return dict(
            desc=self.desc,
            src_dict = self.src_info,
            output=self.output
        )


task_dict = dict()


