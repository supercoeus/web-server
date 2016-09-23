# -*- coding: utf-8 -*-
"""
FileName:   test_mongo_dsl
Author:     Tao Hao
@contact:   
@version:   
Created time:   9/23/16

Description:

Changelog:
"""

from code.mongo_handler import mongo_dsl
import datetime


params = {
    '_start': 1474612452,
    '_end': 1474612500,
    'category': 'all',
    'ip': '1.1.1.1',
    'type': 'cpu'
}

base_dsl = mongo_dsl.BaseDSL()
single_dsl = mongo_dsl.SingleMonitorDataDSL(params=params)


class TestBaseDSL(object):

    def test_get_match(self):
        _start = 1474612452
        _end = 1474612453
        res = base_dsl.get_base_match(_start, _end)
        assert str(res) == str({
            "timestamp": {
                "$gte": datetime.datetime.utcfromtimestamp(_start),
                "$lte": datetime.datetime.utcfromtimestamp(_end)
            }
        })

    def test_get_group_id(self):
        division = 600
        res = base_dsl.get_group_id(division)
        assert str(res) == str({
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
        })


class TestSingleMonitorDataDSL(object):

    def test_get_avg_dsl(self):
        ret = single_dsl.get_avg_dsl()
        # for item in ret:
        assert str(ret) == str([
                {'user': {'$avg': '$user'}},
                {'system': {'$avg': '$system'}},
                {'idle': {'$avg': '$idle'}},
                {'nice': {'$avg': '$nice'}},
                {'iowait': {'$avg': '$iowait'}},
                {'irq': {'$avg': '$irq'}},
                {'softirq': {'$avg': '$softirq'}},
                {'steal': {'$avg': '$steal'}},
                {'guest': {'$avg': '$guest'}},
                {'guest_nice': {'$avg': '$guest_nice'}}
            ])

