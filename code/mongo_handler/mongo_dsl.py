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


class BaseDSL(object):

    def __init__(self, params):
        self.params = params

    def get_base_filter(self):

        return None


class SingleMonitorDataDSL(BaseDSL):

    def __init__(self, params):
        super().__init__()
        self._start = params.get('_start')
        self._end = params.get('_end')
        self.category = params.get('category')

    def gen_dsl(self):

        return {}


class CmpMonitorDataDSL(object):

    def __init__(self, params):
        self._start = params.get('_start')
        self._end = params.get('_end')
        self.category = params.get('category')
        self.ips = params.get('ip[]')

    def gen_dsl(self):

        return {}



