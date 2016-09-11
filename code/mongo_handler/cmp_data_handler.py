# -*- coding: utf-8 -*-
"""
FileName:   cmp_data_handler
Author:     Tao Hao
@contact:   
@version:   
Created time:   8/28/16

Description:

Changelog:
"""

from basehandler import BaseHandler
import code.utils as utils
import code.logger as logger


cmp_data_logger = logger.get_logger('cmp_data')


class DataHandler(BaseHandler):
    """
    得到mongodb返回的数据,数据格式如下:
        [
          {
            "_id": "172.17.0.6",
            "data": [
              {
                "timestamp": 1473574680000,
                "w1_avg": 0.095,
                "w5_avg": 0.13
              },
              {
                "timestamp": 1473573600000,
                "w1_avg": 0.26333333333333336,
                "w5_avg": 0.2966666666666667
              }
            ]
          },
          {
            "_id": "172.17.0.7",
            "data": [
              {
                "timestamp": 1473574680000,
                "w1_avg": 0.095,
                "w5_avg": 0.13
              },
              {
                "timestamp": 1473573600000,
                "w1_avg": 0.26333333333333336,
                "w5_avg": 0.2966666666666667
              }
            ]
          }
        ]
    """
    def __init__(self, dsl, params):
        super(DataHandler, self).__init__(params)
        self.dsl = dsl
        self.params = params

    def get_data(self):
        """
        返回最终数据给前端
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
            cmp_data_logger.info('[final data to web]: %s' % str(result))
        return result

    def format_data(self, data):
        """
        格式化数据形式,组织成前端需要的数据格式
        {
            "categories": [time1, time2, ...],
            "series": [
                {
                    "name": "172.17.0.6",
                    "data": [x1, x2, ...]
                },
                {
                    "name": "172.17.0.7",
                    "data": [x1, x2, ...]
                },
                ...
            ]
        }
        :param data:
        :return:
        """
        categories = []
        series = []
        for item in data[0].get('data'):
            categories.append(item.get('timestamp'))
        for data_by_id in data:
            name = data_by_id.get('_id')
            category_data = []
            for item_data in data_by_id.get('data'):
                category_data.append(round(item_data.get(
                    self.params.get('category')), 4))
            series.append({
                "name": name,
                "data": category_data
            })
        categories = self.timestamp2str(categories)
        return {
            "categories": categories,
            "series": series
        }

    def add_data_when_none(self, data):
        category = self.params.get('category')
        _start = self.params.get('_start')
        _end = self.params.get('_end')
        division = utils.get_division(_start, _end) * 1000
        _start *= 1000
        _end *= 1000
        for data_by_ip in data:
            item_data = data_by_ip.get('data')
            item_data.sort(key=lambda x: x['timestamp'])
            first_time = pre = item_data[0].get('timestamp')
            last_time = item_data[-1].get('timestamp')
            # 首先处理返回数据中间小时间段没有数据的情况
            for i, v in enumerate(item_data):
                current = v.get('timestamp')
                index = i
                if current - pre > division:
                    while current - pre > division:
                        pre += division
                        add_data = {
                            'timestamp': pre,
                            category: 0
                        }
                        item_data.insert(index, add_data)
                        index += 1
                pre = current
            # 处理返回数据前面部分无数据的情况
            if first_time - _start >= division:
                while first_time - _start >= division:
                    first_time -= division
                    add_data = {
                        'timestamp': first_time,
                        category: 0
                    }
                    item_data.insert(0, add_data)
            # 处理返回数据后段无数据的情况
            if _end - last_time >= division:
                while _end - last_time >= division:
                    last_time += division
                    add_data = {
                        'timestamp': last_time,
                        category: 0
                    }
                    item_data.append(add_data)

        return data


