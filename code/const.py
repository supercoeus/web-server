# -*- coding: utf-8 -*-
"""
FileName:   const
Author:     Tao Hao
@contact:   
@version:   
Created time:   9/4/16

Description:
    constant variable
Changelog:
"""

# 说明：agent以60s为周期采取数据
# 5分钟，300s：直接获取
# 1小时，3600s：按1分钟获取
# 6小时，21600s：按6分钟获取
# 1天，86400s：按半小时获取
# 7天，604800s：按1小时获取
# 15天，1296000s：按6小时获取
TIME_DIVISION = {
    'five_minutes': (300, 10),
    "one_hour": (3600, 60),
    "six_hours": (21600, 360),
    "one_day": (86400, 1800),
    "seven_days": (604800, 3600),
    "fifty_days": (1296000, 21600)
}

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

CATEGORIES = {
    'cpu': ('user', 'system', 'idle', 'nice', 'iowait', 'irq',
                'softirq', 'steal', 'guest', 'guest_nice'),
    'load': ('w1_avg', 'w5_avg', 'w15_avg'),
    'memory': ('total', 'used', 'abs_used', 'free',
               'buffers', 'cached', 'active', 'inactive', 'swap_used')
}

