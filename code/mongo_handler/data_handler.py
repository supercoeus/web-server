# -*- coding: utf-8 -*-
"""
FileName:   data_handler
Author:     Tao Hao
@contact:   
@version:   
Created time:   8/28/16

Description:

Changelog:
"""

from basehandler import BaseHandler
from mongo_db import MongoInstance
from code.exceptions_ import MongodbQueryException
import code.const as const
import code.utils as utils
import code.logger as logger


data_logger = logger.get_logger('data')


class DataHandler(BaseHandler):

    def __init__(self, dsl, params):
        self.dsl = dsl
        self.params = params

    def get_mongo_col(self):
        try:
            mongo_ins = MongoInstance()
            db = mongo_ins.get_database()
            col = mongo_ins.get_col(db, col=self.params.get('type'))
            data_logger.info('[mongo dsl name]: %s' % col.name)
            return col
        except Exception as e:
            data_logger.error('get mongo db collection error: %s' % str(e))
            raise MongodbQueryException('get mongodb collection'
                                        ' error: [%s]' % str(e))

    def get_query_result(self):
        """
        返回数据格式为:
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
        :return:
        """
        col = self.get_mongo_col()
        try:
            raw_result = list(col.aggregate(self.dsl))
            data_logger.info('mongo raw_result: %s' % str(raw_result))
            return raw_result
        except Exception as e:
            data_logger.error('query mongo error: %s' % str(e))
            raise MongodbQueryException('query mongodb error: [%s]' % str(e))

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
        raw_result = self.get_query_result()
        result = {
            "categories": [],
            "series": []
        }
        if raw_result:
            add_none_data = self.add_data_when_none(raw_result)
            hanled_data = self.timestamp2str(add_none_data)
            data_logger.info('[handled data]: %s' % str(hanled_data))
            result = self.format_data(hanled_data)
            data_logger.info('[final data to web]: %s' % str(result))

        return result

    @staticmethod
    def format_data(data):
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
        return {
            "categories": categories,
            "series": series
        }



