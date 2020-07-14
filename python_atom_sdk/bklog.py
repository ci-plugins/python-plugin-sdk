# -*- coding: utf-8 -*-

import sys
import logging


LOG_NAME = "ATOM_LOG"
LOG_FORMAT = "%(bk_ci_placeholder)s%(message)s"
LOG_LEVEL = logging.DEBUG
BK_CI_PLACEHOLDER = "BK_CI_PLACEHOLDER"


def getLogger():
    """
    兼容老版本的方法
    """
    return logger().logger


class MyLoggerAdapter(logging.LoggerAdapter):

    def process(self, msg, kwargs):
        if 'extra' not in kwargs:
            kwargs["extra"] = self.extra
        return msg, kwargs


class ContextFilter(logging.Filter):

    def filter(self, record):
        bk_ci_placeholder = ""
        if hasattr(record, "bk_ci_placeholder") and record.bk_ci_placeholder != BK_CI_PLACEHOLDER:
            bk_ci_placeholder = record.bk_ci_placeholder
        else:
            bk_ci_placeholder = record.levelname.lower()
        record.bk_ci_placeholder = "##[{}]".format(bk_ci_placeholder)
        return True


class logger():

    def __init__(self):
        init_logger = logging.getLogger(LOG_NAME)
        if init_logger.handlers:
            self.logger = init_logger
        else:
            init_logger.setLevel(LOG_LEVEL)
            formatter = logging.Formatter(LOG_FORMAT)
            filter = ContextFilter()

            console = logging.StreamHandler(sys.stdout)
            console.setFormatter(formatter)
            console.addFilter(filter)

            init_logger.addHandler(console)

            extra_dict = {"bk_ci_placeholder": BK_CI_PLACEHOLDER}
            self.logger = MyLoggerAdapter(init_logger, extra_dict)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def command(self, command):
        self.logger.info(command, extra={"bk_ci_placeholder": "command"})

    def group_start(self, msg):
        self.logger.info(msg, extra={"bk_ci_placeholder": "group"})

    def group_end(self):
        self.logger.info("", extra={"bk_ci_placeholder": "endgroup"})


if __name__ == '__main__':

    obj = logger()
    obj.group_start("group1 start")
    obj.info("info is info")
    obj.debug("debug is debug")
    obj.warning("warning is warning")
    obj.error("error is error")
    obj.command("this is a command")
    obj.group_end()

