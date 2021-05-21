# -*- coding: utf-8 -*-

import os
import json

from . import setting
from .bklog import BKLogger


class SetOutput():
    """
    @summary: 设置 插件输出
    """

    _log = BKLogger()

    def __init__(self):
        self.data_path = os.getenv(setting.BK_DATA_DIR, '.')
        self.output_file_name = os.getenv(setting.BK_DATA_OUTPUT, 'output.json')

    def check_output(self, output):
        """
        @summary: 检查 插件输出是否合法
        """
        status = output.get("status", None)
        if not status or status not in setting.BK_ATOM_STATUS.values():
            self._log.error("[check output error]invalid status:{}".format(status))
            exit(-1)

        output_template_type = output.get("type", None)
        if not output_template_type or output_template_type not in setting.BK_OUTPUT_TEMPLATE_TYPE.values():
            self._log.error("[check output error]invalid output_template_type:{}".format(output_template_type))
            exit(-1)

        output_data = output.get("data", {})
        for k, v in output_data.items():
            field_type = v.get("type", None)
            if field_type == setting.BK_OUTPUT_FIELD_TYPE.get("STRING", ""):
                pass
            elif field_type == setting.BK_OUTPUT_FIELD_TYPE.get("ARTIFACT", ""):
                field_value = v.get("value", [])
                if not isinstance(field_value, list):
                    self._log.error("[check output error]invalid field[{}], should be list".format(k))
                    exit(-1)
                for file_path in field_value:
                    if not os.path.exists(file_path):
                        self._log.error("[check output error]invalid field[{}], not exists[{}]".format(k, file_path))
                        exit(-1)
            elif field_type == setting.BK_OUTPUT_FIELD_TYPE.get("REPORT", ""):
                pass
            else:
                self._log.error("[check output error]invalid field type: {}".format(field_type))
                exit(-1)

        return

    def set_output(self, output):
        """
        @summary: 设置 插件执行结果、输出参数
        @param output: 输出参数和执行结果dict
        """
        self.check_output(output)

        output_file_path = os.path.join(self.data_path, self.output_file_name)
        if not os.path.exists(self.data_path):
            try:
                os.mkdir(self.data_path)
            except FileExistsError:
                self._log.debug("mkdir data_path error")
                pass

        with open(output_file_path, 'w') as f:
            json.dump(output, f)
