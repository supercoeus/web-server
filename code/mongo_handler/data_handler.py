# -*- coding: utf-8 -*-
"""
FileName:   data_handler
Author:     Tao Hao
@contact:   
@version:   
Created time:   8/28/16

Description: 单机机器的处理类，从mongodb获取数据，再进行处理

Changelog:
"""

from basehandler import BaseHandler
import code.utils as utils
import code.logger as logger


data_logger = logger.get_logger('data')


class DataHandler(BaseHandler):
    """
    查询mongodb返回数据格式为:
        [
          {
            u'_id': 1472982000000L,
            u'w1_avg': 0.6780434782608691,
            u'w5_avg': 0.5749999999999997
          },
          {
            u'_id': 1472982060000L,
            u'w1_avg': 0.46677966101694923,
            u'w5_avg': 0.5303389830508473
          },
          {
            u'_id': 1472982120000L,
            u'w1_avg': 0.46728813559322,
            u'w5_avg': 0.516949152542373
          }
        ]
    """

    def __init__(self, dsl, params):
        super(DataHandler, self).__init__(params)
        self.dsl = dsl
        self.params = params

    def add_data_when_none(self, data):
        """
        当时间段没有数据时，要填补那段时间，并把数据设置为0
        注意mongodb返回的数据的时间戳的13位的
        :return:
        """
        data0 = data[0]
        category_list = data0.keys()
        category_list.remove('_id')
        _start = self.params.get('_start')
        _end = self.params.get('_end')
        division = utils.get_division(_start, _end) * 1000
        _start *= 1000
        _end *= 1000
        # pre = _start
        # for item in data:
        first_time = pre = data[0].get('_id')
        last_time = data[-1].get('_id')
        # 首先处理返回数据中间小时间段没有数据的情况
        for i, v in enumerate(data):
            current = v.get('_id')
            index = i
            if current - pre > division:
                while current - pre > division:
                    pre += division
                    item_data = {
                        '_id': pre
                    }
                    for category in category_list:
                        item_data.update({
                            category: 0
                        })
                    data.insert(index, item_data)
                    index += 1
            pre = current
        # 处理返回数据前面部分无数据的情况
        if first_time - _start >= division:
            while first_time - _start >= division:
                first_time -= division
                item_data = {
                    '_id': first_time
                }
                for category in category_list:
                    item_data.update({
                        category: 0
                    })
                data.insert(0, item_data)
        # 处理返回数据后段无数据的情况
        if _end - last_time >= division:
            while _end - last_time >= division:
                last_time += division
                item_data = {
                    '_id': last_time
                }
                for category in category_list:
                    item_data.update({
                        category: 0
                    })
                data.append(item_data)

        return data

    def get_data(self):
        """
        返回最终给前端使用的数据
        :return:
        """
        raw_result = self.get_query_result(self.dsl)
        result = {
            "categories": [],
            "series": []
        }
        if raw_result:
            add_none_data = self.add_data_when_none(raw_result)
            result = self.format_data(add_none_data)
            data_logger.info('[final data to web]: %s' % str(result))

        return result

    def format_data(self, data):
        """
        格式化数据形式，将数据组织成前端需要的形式:
        {
            "categories": [],
            "series": [
                {
                    "name": "w1_avg",
                    "data": []
                },
                {
                    "name": "w5_avg",
                    "data": []
                },
                ...
            ]
        }
        :return:
        """
        categories = []
        series = []
        data0 = data[0]
        series_names = data0.keys()
        series_names.remove('_id')
        temp = {}
        for name in series_names:
            temp.update({
                name: []
            })
        for item in data:
            categories.append(item.get('_id'))
            for name in series_names:
                # 保留4位小数
                temp.get(name).append(round(item.get(name), 4))
        for name in temp.keys():
            item = {
                'name': name,
                'data': temp.get(name)
            }
            series.append(item)
        categories = self.timestamp2str(categories)
        return {
            "categories": categories,
            "series": series
        }


class IpListHandler(BaseHandler):

    def __init__(self, dsl, params):
        super(IpListHandler, self).__init__(params)
        self.dsl = dsl

    def get_data(self):
        result = []
        raw_result = self.get_query_result(self.dsl)
        if raw_result:
            result = self.format_data(data=raw_result)
        return result

    @staticmethod
    def format_data(data):
        """
        mongodb返回的结果形式：
        [
          {
            "_id": "172.17.0.8"
          },
          {
            "_id": "172.17.0.10"
          }
        ]
        格式化后返回的形式：
        [
            "172.17.0.8", "172.17.0.10"
        ]
        :param data:
        :return:
        """
        iplist = []
        for item in data:
            iplist.append(item.get('_id'))
        return iplist
