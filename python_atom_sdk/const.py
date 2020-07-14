# -*- coding: utf-8 -*-

from . import setting


class Status:
    """
    @summary:  插件执行结果定义
    """
    ERROR = setting.BK_ATOM_STATUS.get("ERROR", None)
    FAILURE = setting.BK_ATOM_STATUS.get("FAILURE", None)
    SUCCESS = setting.BK_ATOM_STATUS.get("SUCCESS", None)


class OutputTemplateType:
    """
    @summary:  插件输出模版类型
    """
    DEFAULT = setting.BK_OUTPUT_TEMPLATE_TYPE.get("DEFAULT", None)
    QUALITY = setting.BK_OUTPUT_TEMPLATE_TYPE.get("QUALITY", None)


class OutputFieldType:
    """
    @summary:  插件输出字段类型
    """
    STRING = setting.BK_OUTPUT_FIELD_TYPE.get("STRING", None)
    ARTIFACT = setting.BK_OUTPUT_FIELD_TYPE.get("ARTIFACT", None)
    REPORT = setting.BK_OUTPUT_FIELD_TYPE.get("REPORT", None)


class OutputReportType:
    """
    @summary:  插件输出字段类型为报告时，报告类型
    """
    INTERNAL = setting.BK_OUTPUT_REPORT_TYPR.get("INTERNAL", None)
    THIRDPARTY = setting.BK_OUTPUT_REPORT_TYPR.get("THIRDPARTY", None)
