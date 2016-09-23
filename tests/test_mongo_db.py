# -*- coding: utf-8 -*-
"""
FileName:   test_mongo_db
Author:     Tao Hao
@contact:   
@version:   
Created time:   9/23/16

Description:

Changelog:
"""
from code.mongo_handler import mongo_db
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
import pytest


mongo_ins = mongo_db.MongoInstance()


class TestMongo(object):

    def test_connect(self):
        res = mongo_ins.connect()
        assert isinstance(res, MongoClient)

    def test_get_data_base(self):
        res = mongo_ins.get_database()
        assert isinstance(res, Database)

    @pytest.mark.parametrize('col', [
        'cpu', 'load', 'memory'
    ])
    def test_get_col(self, col):
        res = mongo_ins.get_col(mongo_ins.get_database(), col)
        print col
        assert isinstance(res, Collection)

