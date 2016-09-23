# -*- coding: utf-8 -*-
"""
FileName:   mongo_db
Author:     Tao Hao
@contact:   
@version:   
Created time:   9/4/16

Description: 处理mongodb的连接

Changelog:
"""

from pymongo import MongoClient
import config
import code.exceptions_ as exceptions_
import code.logger as logger

mongo_logger = logger.get_logger('mongo')


class MongoInstance(object):

    def __init__(self):
        self.mongo_db = config.MONGODB_DB
        self.mongo_url = "mongodb://%s:%s@%s:%d/%s" % \
                         (config.MONGODB_USER, config.MONGODB_PASSWD,
                          config.MONGODB_HOST, config.MONGODB_PORT,
                          self.mongo_db)

    def connect(self):
        client = MongoClient(self.mongo_url)
        return client

    def get_database(self):
        client = self.connect()
        db = client.get_database(self.mongo_db)
        return db

    def get_col(self, db, col):
        try:
            if col in config.MONGODB_COLS:
                col_ = db.get_collection(col)
                return col_
        except Exception as e:
            mongo_logger.error("[get mongo collection error]: %s" % str(e),
                               exc_info=True)
            raise exceptions_.MongodbQueryException(str(e))


# if __name__ == '__main__':
#     import datetime
#     import json
#     mongo_ins = MongoInstance()
#     db = mongo_ins.get_database()
#     col = mongo_ins.get_col(db, 'load')
#     pipe_line = [
#         {'$match': {
#             'timestamp': {
#                 '$lte': datetime.datetime(2016, 9, 11, 6, 20),
#                 '$gte': datetime.datetime(2016, 9, 11, 6, 0)
#             }
#         }},
#         {
#             '$group': {
#                 '_id': {
#                     "ip": "$ip",
#                     "timestamp": {
#                         '$subtract': [
#                             {'$subtract': ['$timestamp',
#                                            datetime.datetime(1970, 1, 1, 0,
#                                                              0)]},
#                             {'$mod': [
#                                 {'$subtract': ['$timestamp',
#                                                datetime.datetime(1970, 1, 1, 0,
#                                                                  0)]},
#                                 360000]}
#                         ]
#                     }
#                 },
#                 'w1_avg': {'$avg': '$w1_avg'}
#             },
#         },
#         {
#             "$group": {
#                 "_id": "$_id.ip",
#                 "data": {
#                     "$push": {
#                         "timestamp": "$_id.timestamp",
#                         "w1_avg": "$w1_avg",
#                     }
#                 }
#             }
#         },
#     ]
#     result = list(col.aggregate(pipeline=pipe_line))
#     print json.dumps(result)
