# -*- coding: utf-8 -*-
"""
FileName:   mongo_dsl
Author:     Tao Hao
@contact:   
@version:   
Created time:   8/28/16

Description:

Changelog:
"""

import code.const as const
import datetime
import code.utils as utils
import code.logger as logger


mongo_dsl_logger = logger.get_logger('mongo_dsl')


class BaseDSL(object):

    # def __init__(self, params):
    #     self.params = params

    @staticmethod
    def get_base_match(_start, _end):
        return {
            "timestamp": {
                "$gte": datetime.datetime.utcfromtimestamp(_start),
                "$lte": datetime.datetime.utcfromtimestamp(_end)
            }
        }

    @staticmethod
    def get_group_id(division):
        return {
            "$subtract": [
                {
                    "$subtract": ["$timestamp", datetime.datetime(1970, 1, 1)]
                },
                {
                    "$mod": [
                        {
                            "$subtract": [
                                "$timestamp", datetime.datetime(1970, 1, 1)
                            ]
                        },
                        division * 1000
                    ]
                }
            ]
        }


class SingleMonitorDataDSL(BaseDSL):

    def __init__(self, params):
        # super(SingleMonitorDataDSL, self).__init__(params)
        self._start = params.get('_start')
        self._end = params.get('_end')
        self.category = params.get('category')
        self.type_ = params.get('type')

    def get_avg_dsl(self):
        result = []
        if self.category == 'all':
            categories = const.CATEGORIES.get(self.type_)
            for item in categories:
                result.append({
                    item: {
                        "$avg": '$' + item
                    }
                })
        return result

    def gen_dsl(self):
        division = utils.get_division(self._start, self._end)
        group_ = {
            '_id': self.get_group_id(division)
        }
        if self.category == 'all':
            for avg_item in self.get_avg_dsl():
                group_.update(avg_item)
        else:
            group_.update({
                self.category: {
                    '$avg': '$' + self.category
                }
            })
        pipe_line = [
            {
                '$match': self.get_base_match(self._start, self._end)
            },
            {
                '$group': group_
            },
            {
                '$sort': {"_id": 1}
            }
        ]
        mongo_dsl_logger.info("[mongo dsl result]: %s" % str(pipe_line))
        return pipe_line


class CmpMonitorDataDSL(BaseDSL):

    def __init__(self, params):
        # super(CmpMonitorDataDSL, self).__init__(params)
        self.params = params
        self._start = params.get('_start')
        self._end = params.get('_end')
        self.category = params.get('category')
        self.ips = params.get('ip[]')

    def gen_dsl(self):
        division = utils.get_division(self._start, self._end)
        group_first = {
            '_id': {
                "ip": "$ip",
                "timestamp": self.get_group_id(division)
            },
            self.category: {
                "$avg": "$" + self.category
            }
        }
        group_second = {
            '_id': "$_id.ip",
            "data": {
                "$push": {
                    "timestamp": "$_id.timestamp",
                    self.category: "$" + self.category
                }
            }
        }
        ip_filter = []
        for ip in self.params.get('iplist'):
            ip_filter.append({
                "ip": ip
            })
        pipe_line = [
            {
                "$match": {
                    "$and": [
                        self.get_base_match(self._start, self._end),
                        {
                            "$or": ip_filter
                        }
                    ]
                }
            },
            {
                "$group": group_first
            },
            {
                "$group": group_second
            }
        ]
        mongo_dsl_logger.info("[mongo dsl result]: %s" % str(pipe_line))
        return pipe_line



