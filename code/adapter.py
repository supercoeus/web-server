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

from mongo_handler import mongo_dsl, data_handler, cmp_data_handler


class MongoAdapter(object):

    @staticmethod
    def get_single_data(params):
        dsl = mongo_dsl.SingleMonitorDataDSL(params)
        dsl_expression = dsl.gen_dsl()
        single_data_handler = data_handler.DataHandler(
            dsl=dsl_expression, params=params
        )
        result = single_data_handler.get_data()
        return result

    @staticmethod
    def get_cmp_data(params):
        dsl = mongo_dsl.CmpMonitorDataDSL(params)
        result = ''
        return result

