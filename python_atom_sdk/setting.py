# -*- coding: utf-8 -*-

BK_SDK_JSON = ".sdk.json"
BK_SDK_JSON_FIELDS = ['buildType', 'projectId', 'agentId', 'secretKey', 'gateway', 'buildId', 'vmSeqId']

# openapi相关
AUTH_HEADER_DEVOPS_BUILD_TYPE = "X-DEVOPS-BUILD-TYPE"
AUTH_HEADER_DEVOPS_PROJECT_ID = "X-DEVOPS-PROJECT-ID"
AUTH_HEADER_DEVOPS_BUILD_ID = "X-DEVOPS-BUILD-ID"
AUTH_HEADER_DEVOPS_VM_SEQ_ID = "X-DEVOPS-VM-SID"
AUTH_HEADER_DEVOPS_AGENT_ID = "X-DEVOPS-AGENT-ID"
AUTH_HEADER_DEVOPS_AGENT_SECRET_KEY = "X-DEVOPS-AGENT-SECRET-KEY"

# 输出输出位置和文件名存储的环境变量名称
BK_DATA_DIR = "bk_data_dir"
BK_DATA_INPUT = "bk_data_input"
BK_DATA_OUTPUT = "bk_data_output"

#  插件输出状态
BK_ATOM_STATUS = {
    "SUCCESS": "success",
    "FAILURE": "failure",
    "ERROR": "error"
}

#  插件输出模版类型
BK_OUTPUT_TEMPLATE_TYPE = {
    "DEFAULT": "default",
    "QUALITY": "quality"
}

#  插件输出字段类型
BK_OUTPUT_FIELD_TYPE = {
    "STRING": "string",
    "ARTIFACT": "artifact",
    "REPORT": "report"
}

# 插件输出为报告时，报告类型
BK_OUTPUT_REPORT_TYPR = {
    "INTERNAL": "INTERNAL",
    "THIRDPARTY": "THIRDPARTY"
}
