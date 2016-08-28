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
FLASK_PORT = '9999'




__set_from_environ()