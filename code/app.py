# -*- coding: utf-8 -*-
"""
FileName:   app
Author:     Tao Hao
@contact:   
@version:   
Created time:   8/28/16

Description:

Changelog:
"""

from flask import Blueprint, request, make_response
import exceptions_
import logger as lg
import adapter

logger = lg.get_logger('web-api')


cpu = Blueprint("cpu", __name__)
memory = Blueprint('memory', __name__)
load = Blueprint('load', __name__)
cpu_s = Blueprint("cpu_s", __name__)
memory_s = Blueprint('memory_s', __name__)
load_s = Blueprint('load_s', __name__)

mongo_adapter = adapter.MongoAdapter()


def check_request_args_single(args, ip):
    _start = args.get('_start', type=int)
    _end = args.get('_end', type=int)
    category = args.get('category', default='all')
    if not _start:
        raise exceptions_.ParamsException("_start should not be none")
    if not _end:
        raise exceptions_.ParamsException("_end should not be none")
    return {
        '_start': _start,
        '_end': _end,
        'category': category,
        'ip': ip
    }


@cpu.route("/<ip>/cpu")
def cpu_info(ip):
    args = request.args
    try:
        params = check_request_args_single(args, ip)

    except exceptions_.BaseDFException as e:
        msg = {
            'status_code': 400,
            'error_code': e.ERROR_CODE,
            'msg': e.msg
        }
        logger.error(msg)




