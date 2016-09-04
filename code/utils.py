# -*- coding: utf-8 -*-
"""
FileName:   utils
Author:     Tao Hao
@contact:   
@version:   
Created time:   8/28/16

Description:

Changelog:
"""

import const
import time
import code.exceptions_ as exceptions_
from code.const import TIME_DIVISION


def timestamp2str(timestamp, full=False):
    """
    将时间戳转换成字符串
    :param timestamp:
    :param full: 若为True则表示是13位时间戳，则要除以1000再进行转换
    :return:
    """
    if full:
        timestamp /= 1000
    return time.strftime(const.TIME_FORMAT, time.localtime(timestamp))


def get_division(_start, _end):
    """
    TIME_DIVISION = {
        'five_minutes': (300, 0),
        "one_hour": (3600, 60),
        "six_hours": (21600, 360),
        "one_day": (86400, 1800),
        "seven_days": (604800, 3600),
        "fifty_days": (129600, 21600)
    }
    :param _start:
    :param _end:
    :return:
    """
    delta = _end - _start
    if delta <= TIME_DIVISION.get('five_minutes')[0]:
        return TIME_DIVISION.get('five_minutes')[1]
    elif TIME_DIVISION.get('five_minutes')[0] < delta \
            <= TIME_DIVISION.get('one_hour')[0]:
        return TIME_DIVISION.get('one_hour')[1]
    elif TIME_DIVISION.get('one_hour')[0] < delta \
            <= TIME_DIVISION.get('six_hours')[0]:
        return TIME_DIVISION.get('six_hours')[1]
    elif TIME_DIVISION.get('six_hours')[0] < delta \
            <= TIME_DIVISION.get('one_day')[0]:
        return TIME_DIVISION.get('one_day')[1]
    elif TIME_DIVISION.get('one_day')[0] < delta \
            <= TIME_DIVISION.get('seven_days')[0]:
        return TIME_DIVISION.get('seven_days')[1]
    elif TIME_DIVISION.get('seven_days')[0] < delta \
            <= TIME_DIVISION.get('fifty_days')[0]:
        return TIME_DIVISION.get('fifty_days')[1]
    else:
        raise exceptions_.ParamsException('_end and start time '
                                          'division is too large')

