# -*- coding: utf-8 -*-
"""
FileName:   exceptions
Author:     Tao Hao
@contact:   
@version:   
Created time:   8/28/16

Description:

Changelog:
"""


class BaseDFException(Exception):

    def __init__(self, msg):
        self.msg = msg


class ParamsException(BaseDFException):
    """
    查询参数错误
    HTTP status_code = 400
    """
    ERROR_CODE = 1000


class MongodbQueryException(BaseDFException):
    """
    mongodb query error
    HTTP status_code = 500
    """
    ERROR_CODE = 1001

