# -*- coding: utf-8 -*-
import inspect
import json
import os
import traceback
from sys import version_info

import requests
from pkg_resources import resource_filename, resource_listdir, resource_isdir

from . import setting
from .bklog import BKLogger


class OpenApi():
    _log = BKLogger()

    def __init__(self):
        sdk_json = self.get_sdk_json()
        self.gateway = sdk_json.get("gateway", None)
        self.header_auth = {
            setting.AUTH_HEADER_DEVOPS_BUILD_TYPE: sdk_json.get("buildType", None),
            setting.AUTH_HEADER_DEVOPS_PROJECT_ID: sdk_json.get("projectId", None),
            setting.AUTH_HEADER_DEVOPS_AGENT_ID: sdk_json.get("agentId", None),
            setting.AUTH_HEADER_DEVOPS_AGENT_SECRET_KEY: sdk_json.get("secretKey", None),
            setting.AUTH_HEADER_DEVOPS_BUILD_ID: sdk_json.get("buildId", None),
            setting.AUTH_HEADER_DEVOPS_VM_SEQ_ID: sdk_json.get("vmSeqId", None)
        }

        # 保存session增加3次重试
        self.session = requests.Session()
        self.session.trust_env = False
        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        self.session.mount('http://', adapter)

    def get_sdk_json(self):
        """
        @summary：获取sdk配置
        """
        sdk_path = os.path.join(os.environ.get(setting.BK_DATA_DIR, None), setting.BK_SDK_JSON)
        if not os.path.exists(sdk_path):
            self._log.error("[openapi]init error: sdk json do not exist")
            exit(-1)

        with open(sdk_path, 'r') as f_sdk:
            content = f_sdk.read()
        if not content:
            self._log.error("[openapi]init error: sdk json is null")
            exit(-1)

        try:
            sdk_json = json.loads(content)

            check_result, field = self.check_sdk_json(sdk_json)
            if not check_result:
                self._log.error("[openapi]check sdk json field error: {}".format(field))
                exit(-1)

            return sdk_json
        except Exception as _e:  # pylint: disable=broad-except
            self._log.error("[openapi]parse sdk json error, sdk.json is {}".format(content))
            print(traceback.format_exc())
            exit(-1)

    def check_sdk_json(self, src_json):
        """
        @summary：检查sdk配置
        """
        for field in setting.BK_SDK_JSON_FIELDS:
            if not src_json.get(field, None):
                return False, field

        return True, ""

    def generate_url(self, path):
        """
        @summary：组装访问openapi的url
        """
        if self.gateway.startswith("http://") or self.gateway.startswith("https://"):
            return "{}/{}".format(self.gateway, path.lstrip("/"))
        else:
            return "http://{}/{}".format(self.gateway, path.lstrip("/"))

    def process_response(self, res):
        try:
            if res.status_code == 200:
                ret = res.json()
                if ret["status"] != 0:
                    self._log.error("unexpected status: {}, content is {}".format(ret["status"], ret))
                    return False, {}

                return True, ret["data"]
            else:
                msg = res.json().get("message", "")
                if version_info.major == 2:
                    msg = msg.encode("utf-8")
                self._log.error("unexpected status_code: {}, message is {}".format(res.status_code, msg))
                return False, {}
        except Exception as _e:  # pylint: disable=broad-except
            self._log.error(repr(res.text))
            print(traceback.format_exc())
            return False, {}

    def do_get(self, url, params=None, timeout=60):
        # self._log.debug(url)
        if params:
            res = self.session.get(url, headers=self.header_auth, params=params, timeout=timeout)
        else:
            res = self.session.get(url, headers=self.header_auth, timeout=timeout)

        return self.process_response(res)

    def do_post(self, url, header=None, message=None, timeout=120):
        for key, val in header.items():
            self.header_auth[key] = val

        with self.session as session:
            if message:
                res = session.post(url, headers=self.header_auth, data=json.dumps(message), timeout=timeout)
            else:
                res = session.post(url, headers=self.header_auth, timeout=timeout)

            return self.process_response(res)

    def get_credential(self, credential_id):
        """
        @summary：根据凭据ID，获取凭据内容
        """

        path = "/ticket/api/build/credentials/{}/detail".format(credential_id)
        url = self.generate_url(path)
        return self.do_get(url)

    def get_repo_info(self, identity, identity_type):
        """
        @summary：根据代码库别名，获取代码库详细地址
        """
        path = "/repository/api/build/repositories/"
        params = {
            "repositoryId": identity,
            "repositoryType": identity_type
        }
        url = self.generate_url(path)

        return self.do_get(url, params=params)

    def get_context_by_name(self, context_name):
        path = "/process/api/build/variable/get_build_context?contextName={}&check=true" \
            .format(context_name)
        url = self.generate_url(path)
        return self.do_get(url)


    def get_caller_project_package_name(self):
        # 获取调用栈帧
        stack_frames = inspect.stack()

        # 查找调用 SDK 的项目包名
        for frame in stack_frames:
            module_name = frame[0].f_globals['__name__']
            # 如果模块名不是 SDK 包名，认为找到了调用项目的包名
            if not module_name.startswith('python_atom_sdk'):
                project_package_name = module_name.split('.')[0]
                return project_package_name

        return None

    def get_message_by_locale(self, project_package_name, message_code, language, error_code, default_msg):
        """
        @summary：根据语言环境获取对应的描述信息
        :param message_code：消息标识
        :param language：语言信息
        :param error_code：错误码
        :param default_msg：默认信息
        :return: 描述信息
        """
        try:
            file_name = "message_{}.properties".format(language)
            file_dir = resource_filename(project_package_name, 'i18n/' + file_name)
            if not os.path.exists(file_dir):
                self._log.warning("Fail to get i18nMessage, the file {} was not found".format(file_name))
                return default_msg

            properties = {}
            with open(file_dir, 'r', encoding='utf-8') as pro_file:
                for line in pro_file.readlines():
                    if line.find('=') > 0:
                        strs = line.replace('\n', '').split('=')
                        properties[strs[0].strip()] = strs[1]

            if error_code:
                if isinstance(message_code, list) and message_code:
                    return properties[str(error_code)].format(*message_code)
                return properties[str(error_code)].format(message_code)
            else:
                return properties[str(message_code)]
        except IndexError:
            self._log.warning("Fail to get i18nMessage, [message_code] formatting failed."
                              " The number of list parameters does not match that of formatting parameters")
            return default_msg
        except UnicodeDecodeError as o:
            self._log.warning("Fail to get i18nMessage, UnicodeDecodeError: {}".format(o))
            return default_msg
        except UnicodeError as s:
            self._log.warning("Fail to get i18nMessage, UnicodeError: {}".format(s))
            return default_msg
        except KeyError:
            self._log.warning("Fail to get i18nMessage of messageCode[{0}], KeyError: '{0}'".format(message_code))
            return default_msg
        except Exception as e:
            self._log.warning("Fail to get i18nMessage, {}".format(e))
            return default_msg

