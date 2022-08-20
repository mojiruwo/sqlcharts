#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os

sql_json_url = './dist/json/sql_data.json'
sql_er_url = './dist/json/sql_er.json'


def mod(a, b):
    c = a // b
    r = a - c * b
    return r


def writeJson(data, filename, format=False):
    with open(filename, 'w') as file_obj:
        if format:
            json.dump(data, file_obj, indent=4)
        else:
            json.dump(data, file_obj)


def readJson(filename):
    if os.path.exists(filename) == False:
        return
    with open(filename, 'r', encoding='utf-8') as f:
        try:
            while True:
                line = f.readline()
                if line:
                    r = json.loads(line)
                    return r
                else:
                    break
        except:
            f.close()
