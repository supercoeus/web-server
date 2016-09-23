# -*- coding: utf-8 -*-
"""
FileName:   test_app
Author:     Tao Hao
@contact:   
@version:   
Created time:   9/17/16

Description:

Changelog:
"""
import pytest
from code import app, const
from werkzeug.datastructures import MultiDict
from code import exceptions_
import json
import requests
import urllib


HOST = 'http://172.17.0.6:9999/api/v1'


@pytest.mark.parametrize('args, types, ip, single, flag', [
    (
        MultiDict([
            ('_start', 1474104368),
            ('_end', 1474114008),
        ]),
        ['cpu', 'load', 'memory'], '1.1.1.1', True, '1'
    ),
    (
        MultiDict([
            ('_start', 1474114008),
            ('_end', 1474104368),
        ]),
        ['cpu', 'load', 'memory'], '1.1.1.1', True, '2'
    ),
    (
        MultiDict([
        ]),
        ['cpu', 'load', 'memory'], '1.1.1.1', True, '3'
    ),
    (
        MultiDict([
            ('_start', 1474104368),
            ('_end', 1474114008),
            ('ip[]', '1.1.1.1'),
            ('ip[]', '2.2.2.2')
        ]),
        ['cpu', 'load', 'memory'], None, False, '4'
    ),
    (
        MultiDict([
            ('_start', 1474104368),
            ('_end', 1474114008),
        ]),
        ['cpu', 'load', 'memory'], None, False, '5'
    ),
    (
        MultiDict([
            ('_start', 1474104368),
            ('_end', 1474114008),
            ('ip[]', '1.1.1.1'),
            ('ip[]', '2.2.2.2')
        ]),
        ['cpu', 'load', 'memory'], None, False, '6'
    )

])
def test_check_request_args(args, types, ip, single, flag):
    for type_ in types:
        for category in const.CATEGORIES.get(type_):
            if flag != '4':
                args.add('category', category)
                if flag == '1':
                    res = app.check_request_args(args, type_, ip, single)
                    data = {
                        '_start': 1474104368,
                        '_end': 1474114008,
                        'category': category,
                        'ip': '1.1.1.1',
                        'type': type_
                    }
                    assert json.dumps(data) == json.dumps(res)
                elif flag == '6':
                    res = app.check_request_args(args, type_, ip, single)
                    data = {
                        '_start': 1474104368,
                        '_end': 1474114008,
                        'category': category,
                        'type': type_,
                        'iplist': ['1.1.1.1', '2.2.2.2']
                    }
                    assert json.dumps(data) == json.dumps(res)
                else:
                    try:
                        res = app.check_request_args(args, type_, ip, single)
                    except exceptions_.ParamsException as e:
                        if flag == '2':
                            assert '_end time should be larger' in str(e.msg)
                        elif flag == '3':
                            assert 'should not be none' in str(e.msg)
                        elif flag == '5':
                            assert 'ip list is None' in str(e.msg)
            else:
                args.add('category', category)
                try:
                    res = app.check_request_args(args, type_, ip, single)
                except exceptions_.ParamsException as e:
                    assert 'category is wrong' in str(e.msg)
            args.pop('category')


@pytest.mark.parametrize('url, url_type', [
    ('/machine/1.1.1.1/', 'cpu'),
    ('/machine/1.1.1.1/', 'load'),
    ('/machine/1.1.1.1/', 'memory'),
    ('/machine/1.1.1.1/', 'test'),
    ('/machines/', 'cpu'),
    ('/machines/', 'load'),
    ('/machines/', 'memory'),
    ('/machines/', 'test'),
])
def test_machine_info(app, url, url_type):
    api = '/api/v1' + url + url_type
    with app.test_client() as client:
        params = {
             '_start': 1474104368,
             '_end': 1474114008,
        }
        if url_type == 'test':
            params.update({'category': 'user'})
            # res = requests.get(api, params=params)
            res = client.get(api, query_string=urllib.urlencode(params))
            assert res.status_code == 404
            assert '"error_code": 1002' in res.data
        else:
            query_string = urllib.urlencode(params)
            if url == '/machines/':
                query_string += '&ip[]=1.1.1.1&ip[]=2.2.2.2'
            categories = const.CATEGORIES.get(url_type) + ('test',)
            for category in categories:
                # params.update({
                #     'category': category
                # })
                res = client.get(api, query_string=query_string + '&category=%s' % category)
                if category == 'test':
                    assert res.status_code == 400
                    assert '"error_code": 1000' in res.data
                else:
                    assert res.status_code == 200


def test_get_iplist(app):
    api = '/api/v1' + '/ips'
    with app.test_client() as client:
        res = client.get(api)
        assert res.status_code == 200


def test_test(app):
    api = '/api/v1/'
    with app.test_client() as client:
        res = client.get(api)
        assert res.status_code == 200






