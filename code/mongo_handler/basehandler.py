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
from mongo_db import MongoInstance
import code.logger as logger
from code.exceptions_ import MongodbQueryException


bh_logger = logger.get_logger('base_handler')


class BaseHandler(object):

    def __init__(self, params):
        self.params = params

    @staticmethod
    def timestamp2str(categories):
        for i, v in enumerate(categories):
            categories[i] = utils.timestamp2str(v, full=True)
        return categories

    def get_mongo_col(self):
        try:
            mongo_ins = MongoInstance()
            db = mongo_ins.get_database()
            col = mongo_ins.get_col(db, col=self.params.get('type'))
            bh_logger.info('[mongo dsl name]: %s' % col.name)
            return col
        except Exception as e:
            bh_logger.error('get mongo db collection error: %s' % str(e),
                            exc_info=True)
            raise MongodbQueryException('get mongodb collection'
                                        ' error: [%s]' % str(e))

    def get_query_result(self, dsl):
        col = self.get_mongo_col()
        try:
            raw_result = list(col.aggregate(dsl))
            bh_logger.info('mongo raw_result: %s' % str(raw_result))
            return raw_result
        except Exception as e:
            bh_logger.error('query mongo error: %s' % str(e), exc_info=True)
            raise MongodbQueryException('query mongodb error: [%s]' % str(e))

