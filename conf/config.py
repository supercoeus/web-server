# -*- coding: utf-8 -*-
"""
FileName:   config
Author:     Tao Hao
@contact:   
@version:   
Created time:   8/28/16

Description:

Changelog:
"""


import os


def __set_from_environ():
    d = globals()
    for k in d:
        v = os.environ.get(k)
        if v:
            if v == 'False':
                v = False
            elif v == 'True':
                v = True
            d[k] = v

FLASK_HOST = '0.0.0.0'
FLASK_PORT = 9999

MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DB = 'mongo'
MONGODB_USER = 'mongo'
MONGODB_PASSWD = 'mongo'
MONGODB_COLS = ('cpu', 'load', 'memory')


__set_from_environ()

