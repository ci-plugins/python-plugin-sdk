# -*- coding: utf-8 -*-
import os

from .bklog import BKLogger, getLogger
from .const import Status, OutputTemplateType, OutputFieldType, OutputReportType, OutputErrorType
from .input import ParseParams
from .output import SetOutput

log = BKLogger()
parseParamsObj = ParseParams()
params = parseParamsObj.get_input()
status = Status()
output_template_type = OutputTemplateType()
output_field_type = OutputFieldType()
output_report_type = OutputReportType()
output_error_type = OutputErrorType()


def get_input():
    """
    @summary: 获取 插件输入参数
    @return dict
    """
    return params


def get_project_name():
    """
    @summary: 获取项目英文名
    """
    return params.get("project.name", None)


def get_project_name_cn():
    """
    @summary: 获取项目中文名
    """
    return params.get("project.name.chinese", None)


def get_pipeline_id():
    """
    @summary: 获取流水线ID
    """
    return params.get("pipeline.id", None)


def get_pipeline_name():
    """
    @summary: 获取流水线名称
    """
    return params.get("pipeline.name", None)


def get_pipeline_build_id():
    """
    @summary: 获取buildId
    """
    return params.get("pipeline.build.id", None)


def get_pipeline_build_num():
    """
    @summary: 获取buildno
    """
    return params.get("pipeline.build.num", None)


def get_pipeline_start_type():
    """
    @summary: 获取流水线启动类型
    """
    return params.get("pipeline.start.type", None)


def get_pipeline_start_user_id():
    """
    @summary: 获取流水线启动人
    """
    return params.get("pipeline.start.user.id", None)


def get_pipeline_start_user_name():
    """
    @summary: 获取流水线启动人
    """
    return params.get("pipeline.start.user.name", None)


def get_pipeline_creator():
    """
    @summary: 获取流水线创建人
    """
    return params.get("BK_CI_PIPELINE_CREATE_USER", None)


def get_pipeline_modifier():
    """
    @summary: 获取流水线最近修改人
    """
    return params.get("BK_CI_PIPELINE_UPDATE_USER", None)


def get_pipeline_time_start_mills():
    """
    @summary: 获取流水线启动时间
    """
    return params.get("pipeline.time.start", None)


def get_pipeline_version():
    """
    @summary: 获取流水线的版本
    """
    return params.get("pipeline.version", None)


def get_workspace():
    """
    @summary: 获取工作空间
    """
    return params.get("bkWorkspace", None)


def get_test_version_flag():
    """
    @summary: 当前插件是否是测试版本标识
    """
    return params.get("testVersionFlag", None)


def get_sensitive_conf(key):
    """
    @summary: 获取配置数据
    """
    conf_json = params.get("bkSensitiveConfInfo", None)
    if conf_json:
        return conf_json.get(key, None)
    else:
        return None


def set_output(output):
    """
    @summary: 设置输出
    """
    setOutput = SetOutput()
    setOutput.set_output(output)


def get_credential(credential_id):
    from .openapi import OpenApi
    client = OpenApi()
    return client.get_credential(credential_id)


def get_repo_info(identity, identity_type):
    """
    @summary: 获取代码库信息
    """
    from .openapi import OpenApi
    client = OpenApi()
    return client.get_repo_info(identity, identity_type)


def get_context_by_name(context_name):
    from .openapi import OpenApi
    client = OpenApi()
    return client.get_context_by_name(context_name)


def get_language():
    language = os.getenv("BK_CI_LOCALE_LANGUAGE", "zh_CN")
    return language


def prepare_i18n_environment(package_name):
    import os
    import shutil
    if not os.path.exists('i18n'):
        print("The 'i18n' directory does not exist.")
        return
    try:
        shutil.copytree('i18n', f'{package_name}/i18n', dirs_exist_ok=True)
    except FileExistsError:
        for root, dirs, files in os.walk('i18n'):
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(f'{package_name}/i18n', file)
                shutil.copy2(src_file, dst_file)
    else:
        for root, dirs, files in os.walk('i18n'):
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(f'{package_name}/i18n', file)
                if os.path.exists(dst_file):
                    os.remove(dst_file)
                shutil.copy2(src_file, dst_file)


def get_message_by_locale(messageCode, error_code=None, default_msg=""):
    """
    @summary：根据语言环境获取对应的描述信息
    :param messageCode: task.json文件中key(消息标识)或替换描述信息占位符的参数数组
    :param error_code: 插件错误码
    :param default_msg: 未获取到国际化信息时返回的默认信息
    :return: 描述信息
    """
    from .openapi import OpenApi
    client = OpenApi()
    language = get_language()
    project_package_name = client.get_caller_project_package_name()
    return client.get_message_by_locale(
        project_package_name=project_package_name,
        message_code=messageCode,
        language=language,
        error_code=error_code,
        default_msg=default_msg
    )


if __name__ == "__main__":
    pass
