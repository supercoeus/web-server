# -*- coding: utf-8 -*-
"""
FileName:   testconf
Author:     Tao Hao
@contact:   
@version:   
Created time:   9/23/16

Description:

Changelog:
"""
import pytest
import code.__main__ as main
from flask import Flask


@pytest.fixture
def app():
    app_ = Flask(__name__)
    main.register_site(app_)
    return app_

