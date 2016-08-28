# -*- coding: utf-8 -*-
"""
FileName:   logger
Author:     Tao Hao
@contact:   
@version:   
Created time:   8/27/16

Description:

Changelog:
"""

import logging


LOGGER_FORMAT = "%(asctime)s %(levelname) 8s: [%(filename)s:%(lineno)d]" \
                    " [%(processName)s] - %(message)s"
DATE_FORMAT = '[%Y-%m-%d %H:%M:%S]'


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    strm_handler = logging.StreamHandler()
    strm_handler.setFormatter(logging.Formatter(LOGGER_FORMAT, DATE_FORMAT))
    logger.addHandler(strm_handler)
    logger.setLevel(logging.INFO)
    return logger


if __name__ == '__main__':
    logger = get_logger("test")
    logger.info("aaa")
    logger.error("errorrr!!!")

