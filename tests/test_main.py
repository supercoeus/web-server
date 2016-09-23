
# -*- coding: utf-8 -*-
"""
FileName:   test_main
Author:     Tao Hao
@contact:   
@version:   
Created time:   9/23/16

Description:

Changelog:
"""
import code.__main__ as main
import pytest
from flask import url_for
import multiprocessing


def test_register_site(app):
    main.register_site(app)
    assert url_for('machine.single_machine_info', ip='1.1.1.1', type_='cpu') \
        == '/api/v1/machine/1.1.1.1/cpu'
    assert url_for('machines.machines_info', type_='cpu') \
        == '/api/v1/machines/cpu'
    assert url_for('iplist.get_iplist') == '/api/v1/ips'


def test_main(app):
    # main.main()
    # p = multiprocessing.Process(target=main.main)
    # p.daemon = True
    # p.start()
    with app.test_client() as client:
        assert client.get('/api/v1/aaa').status_code == 404
    # p.terminate()


