# -*- coding: utf-8 -*-
"""
FileName:   __main__
Author:     Tao Hao
@contact:   
@version:   
Created time:   8/28/16

Description:

Changelog:
"""
from flask import Flask, make_response, jsonify
# from app import cpu, cpu_s, memory, memory_s, load, load_s
import config
from app import machine, machines


def register_site(app):
    app.register_blueprint(machine, url_prefix='/api/v1')
    # app.register_blueprint(memory, url_prefix='/api/v1')
    # app.register_blueprint(load, url_prefix='/api/v1')
    # app.register_blueprint(cpu_s, url_prefix='/api/v1/machines')
    app.register_blueprint(machines, url_prefix='/api/v1/machines')
    # app.register_blueprint(load_s, url_prefix='/api/v1/machines')


def main():
    app = Flask(__name__)
    register_site(app)

    @app.errorhandler(404)
    def handle_404(error):
        msg = {
            'status_code': 404,
            'error_code': 1002,
            'msg': 'resource not exist:  %s' % str(error)
        }
        return make_response(jsonify(msg), 404)

    @app.errorhandler(Exception)
    def unknown_exception(error):
        msg = {
            'status_code': 500,
            'error_code': 1003,
            'msg': 'unknown error:  %s' % str(error)
        }
        return make_response(jsonify(msg), 500)

    app.run(config.FLASK_HOST, config.FLASK_PORT)


if __name__ == '__main__':
    main()


