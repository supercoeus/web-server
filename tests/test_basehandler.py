# -*- coding: utf-8 -*-
"""
FileName:   test_basehandler
Author:     Tao Hao
@contact:   
@version:   
Created time:   9/23/16

Description:

Changelog:
"""

from code.mongo_handler import basehandler
import pytest
from pymongo import collection
import json


params = {
    '_start': 1474612452,
    '_end': 1474612500,
    'category': 'sys',
    'ip': '1.1.1.1',
    'type': 'cpu'
}

bh = basehandler.BaseHandler(params)


class TestBaseHandler(object):

    @pytest.mark.parametrize('categories, result', [
        ([1474612452000, 1474612453000],
         ['2016-09-23 14:34:12', '2016-09-23 14:34:13'])
    ])
    def test_timestamp2str(self, categories, result):
        assert str(bh.timestamp2str(categories=categories)) == str(result)

    def test_get_mongo_col(self):
        assert isinstance(bh.get_mongo_col(), collection.Collection)

    def test_get_query_result(self):
        dsl = [
            {
                '$group': {
                    "_id": "$ip",
                }
            }
        ]
        for item in bh.get_query_result(dsl=dsl):
            assert item in [{'_id': '172.17.0.5'}, {'_id': '172.17.0.11'},
             {'_id': '172.17.0.12'}, {'_id': '172.17.0.10'},
             {'_id': '172.17.0.9'}, {'_id': '172.17.0.8'},
             {'_id': '172.17.0.6'}]

