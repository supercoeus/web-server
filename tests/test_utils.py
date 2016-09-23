# -*- coding: utf-8 -*-
"""
FileName:   test_utils
Author:     Tao Hao
@contact:   
@version:   
Created time:   9/23/16

Description:

Changelog:
"""
from code import utils
import pytest
from code.const import TIME_DIVISION


def test_timestamp2str():
    assert utils.timestamp2str(timestamp=1474612452) == '2016-09-23 14:34:12'
    assert utils.timestamp2str(1474612452000, full=True) \
        == '2016-09-23 14:34:12'


@pytest.mark.parametrize('_start, _end, time_name', [
    (1474612452, 1474612652, 'five_minutes'),
    (1474612452, 1474613452, 'one_hour'),
    (1474612452, 1474622452, 'six_hours'),
    (1474612452, 1474912452, 'seven_days'),
    (1474612452, 1474672452, 'one_day'),
    (1474612452, 1475612452, 'fifty_days')
])
def test_get_division(_start, _end, time_name):
    assert utils.get_division(_start, _end) == TIME_DIVISION.get(time_name)[1]



