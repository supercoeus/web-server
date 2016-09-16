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

from flask import Blueprint, request, make_response, jsonify
import exceptions_
import logger as lg
import adapter
import const

logger = lg.get_logger('web-api')


# cpu = Blueprint("cpu", __name__)
# memory = Blueprint('memory', __name__)
# load = Blueprint('load', __name__)
# cpu_s = Blueprint("cpu_s", __name__)
# memory_s = Blueprint('memory_s', __name__)
# load_s = Blueprint('load_s', __name__)

machine = Blueprint("machine", __name__)
machines = Blueprint('machines', __name__)
iplist = Blueprint('iplist', __name__)

mongo_adapter = adapter.MongoAdapter()


def check_request_args(args, type_, ip=None, single=True):
    _start = args.get('_start', type=int)
    _end = args.get('_end', type=int)
    if not _start:
        raise exceptions_.ParamsException("_start should not be none")
    if not _end:
        raise exceptions_.ParamsException("_end should not be none")
    if _start >= _end:
        raise exceptions_.ParamsException("_end time should be larger "
                                          "than _start")
    if single:
        category = args.get('category', default='all')
        if category != 'all' and category not in const.CATEGORIES.get(type_):
            raise exceptions_.ParamsException('category is wrong')
        params = {
            '_start': _start,
            '_end': _end,
            'category': category,
            'ip': ip,
            'type': type_
        }
    else:
        category = args.get('category')
        if not category or category not in const.CATEGORIES.get(type_):
            raise exceptions_.ParamsException('category is wrong')
        iplist = args.getlist('ip[]')
        if not iplist:
            raise exceptions_.ParamsException('ip list is None')
        params = {
            '_start': _start,
            '_end': _end,
            'category': category,
            'iplist': iplist,
            'type': type_
        }
    logger.info('[parse params]: %s' % str(params))
    return params


@machine.route('/')
def test():
    return "test"


@machine.route("/machine/<ip>/<type_>")
def single_machine_info(ip, type_):
    args = request.args
    if type_ not in ('cpu', 'load', 'memory'):
        msg = {
            'status_code': 404,
            'error_code': 1002,
            'msg': '[%s] is not exist' % type_
        }
        logger.error(msg)
        return make_response(jsonify(msg), 404)
    try:
        params = check_request_args(args, type_, ip, single=True)
        result = mongo_adapter.get_single_data(params)
        return jsonify(result)
    except exceptions_.BaseDFException as e:
        msg = {
            'status_code': e.HTTP_STATUS_CODE,
            'error_code': e.ERROR_CODE,
            'msg': e.msg
        }
        logger.error(msg)
        return make_response(jsonify(msg), e.HTTP_STATUS_CODE)


@machines.route("/machines/<type_>")
def machines_info(type_):
    args = request.args
    if type_ not in ('cpu', 'load', 'memory'):
        msg = {
            'status_code': 404,
            'error_code': 1002,
            'msg': '[%s] is not exist' % type_
        }
        logger.error(msg)
        return make_response(jsonify(msg), 404)
    try:
        params = check_request_args(args, type_, ip=None, single=False)
        result = mongo_adapter.get_cmp_data(params)
        return jsonify(result)
    except exceptions_.BaseDFException as e:
        msg = {
            'status_code': e.HTTP_STATUS_CODE,
            'error_code': e.ERROR_CODE,
            'msg': e.msg
        }
        logger.error(msg)
        return make_response(jsonify(msg), e.HTTP_STATUS_CODE)


@iplist.route("/ips")
def get_iplist():
    try:
        result = mongo_adapter.get_iplist()
        return jsonify(result)
    except exceptions_.BaseDFException as e:
        msg = {
            'status_code': e.HTTP_STATUS_CODE,
            'error_code': e.ERROR_CODE,
            'msg': e.msg
        }
        logger.error(msg)
        return make_response(jsonify(msg), e.HTTP_STATUS_CODE)



