# -*- coding: utf-8 -*-
import os
import traceback
import requests
import requests_toolbelt as rt
from sys import version_info
import json

from . import setting
from .bklog import logger


class OpenApi():
    _log = logger()

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
        except Exception as _e: # pylint: disable=broad-except
            self._log.error("[openapi]parse sdk json error, sdk.json is {}" .format(content))
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
        except Exception as _e: # pylint: disable=broad-except
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
