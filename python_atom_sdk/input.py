# -*- coding: utf-8 -*-

import os
import json
import codecs
import sys

from . import setting
from .bklog import logger


class ParseParams():
    """
    @summary: 获取 插件入参
    """

    _log = logger()

    def __init__(self):
        self.data_path = os.getenv(setting.BK_DATA_DIR, '.')
        self.input_file_name = os.getenv(setting.BK_DATA_INPUT, 'input.json')

    def get_input(self):
        """
        @summary: 获取 插件输入参数
        @return dict
        """
        input_file_path = os.path.join(self.data_path, self.input_file_name)
        # self._log.info("input_file_path: {}".format(input_file_path))
        if os.path.exists(input_file_path):
            if sys.version_info.major == 2:
                with codecs.open(input_file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    return json.loads(content)
            else:
                with open(input_file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    return json.loads(content)

        return {}
