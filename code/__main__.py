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
from flask import Flask
from app import cpu, cpu_s, memory, memory_s, load, load_s
import config


def register_site(app):
    app.register_blueprint(cpu, url_prefix='/api/v1')
    app.register_blueprint(memory, url_prefix='/api/v1')
    app.register_blueprint(load, url_prefix='/api/v1')
    app.register_blueprint(cpu_s, url_prefix='/api/v1/machines')
    app.register_blueprint(memory_s, url_prefix='/api/v1/machines')
    app.register_blueprint(load_s, url_prefix='/api/v1/machines')


def main():
    app = Flask(__name__)
    register_site(app)

    @app.error_handlers(404)
    def handle_404():
        pass

    @app.error_handlers(Exception)
    def unknown_exception():
        pass

    app.run(config.FLASK_HOST, config.FLASK_PORT)


if __name__ == '__main__':
    main()


