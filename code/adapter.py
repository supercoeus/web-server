# -*- coding: utf-8 -*-
"""
FileName:   adapter
Author:     Tao Hao
@contact:   
@version:   
Created time:   8/28/16

Description:

Changelog:
"""

from mongo_handler import mongo_dsl


class MongoAdapter(object):

    @staticmethod
    def get_single_data(params):
        dsl = mongo_dsl.SingleMonitorDataDSL(params)
        result = ''
        return result

    @staticmethod
    def get_cmp_data(params):
        dsl = mongo_dsl.CmpMonitorDataDSL(params)
        result = ''
        return result

