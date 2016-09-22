# -*- coding: utf-8 -*-
"""
FileName:   adapter
Author:     Tao Hao
@contact:   
@version:   
Created time:   8/28/16

Description: 这是将请求和数据处理联系起来的部分。adapter获取mongodb的查询语句，
再通过查询语句调用其他类的方法得到前端最终要的结果，再返回给请求处理部分。

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
        del_expression = dsl.gen_dsl()
        cmp_handler = cmp_data_handler.DataHandler(
            dsl=del_expression, params=params)
        result = cmp_handler.get_data()
        return result

    @staticmethod
    def get_iplist():
        params = {
            "type": "load"
        }
        dsl_expression = mongo_dsl.IpListDSL.gen_dsl()
        iplist_handler = data_handler.IpListHandler(
            dsl=dsl_expression, params=params
        )
        result = iplist_handler.get_data()
        return result


