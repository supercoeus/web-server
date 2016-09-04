# -*- coding: utf-8 -*-
"""
FileName:   basehandler
Author:     Tao Hao
@contact:   
@version:   
Created time:   9/4/16

Description:

Changelog:
"""
import code.utils as utils


class BaseHandler(object):

    @staticmethod
    def timestamp2str(data):
        for item in data:
            item['_id'] = utils.timestamp2str(item.get('_id'), full=True)
        return data

    # @staticmethod
    # def add_data_when_none(data):
    #     """
    #     当时间段没有数据时，要填补那段时间，并把数据设置为0
    #     :return:
    #     """

