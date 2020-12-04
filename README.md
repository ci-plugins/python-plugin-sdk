# python-plugin-sdk

ci pipeline plugin sdk for python

## SDK用途

协助使用Python语言开发插件的开发者快速实现插件功能

## SDK用法

- 将SDK模块拷贝至插件代码目录下
  - [插件示例](https://github.com/ci-plugins/plugin-demo-python)
- 在requirement.txt中增加如下申明
  - requests==2.20.1
  - requests-toolbelt==0.9.1
- 使用时，导入SDK

```python
# -*- coding: utf-8 -*-

import python_atom_sdk
```

## SDK常量

- 状态
  - python_atom_sdk.status.SUCCESS  # 成功
  - python_atom_sdk.status.FAILURE  # 失败
  - python_atom_sdk.status.ERROR    # 异常

- 输出模版类型
  - python_atom_sdk.output_template_type.DEFAULT  # 默认
  - python_atom_sdk.output_template_type.QUALITY  # 质量红线

- 输出字段类型
  - python_atom_sdk.output_field_type.STRING    # 字符串
  - python_atom_sdk.output_field_type.ARTIFACT  # 构件
  - python_atom_sdk.output_field_type.REPORT    # 报告

- 错误类型
  - python_atom_sdk.output_error_type.USER             # 用户配置、使用方式错误
  - python_atom_sdk.output_error_type.THIRD_PARTY      # 第三方系统错误
  - python_atom_sdk.output_error_type.PLUGIN           # 插件错误

## SDK方法

### 获取工作空间

- 方法名：get_workspace
- 功能说明：
获取工作空间
- 输入参数：
无
- 返回：
类型：string

### 获取插件输入

- 方法名：get_input
- 功能说明：
获取插件执行时的输入参数信息
- 输入参数：
无
- 返回：
  - 类型：dict
  - 示例：
    ```json
    {
        "input_1": "value1",
        "input_2": "value2"
    }
    ```
  - 获取其中一个入参： ret.get("input_1", None)
  - **注意，值都是字符串**

### 获取当前项目英文名称

- 方法名：get_project_name
- 功能说明：
获取当前执行的流水线所属项目英文名称
- 输入参数：
无
- 返回：
类型：string

### 获取当前项目中文名

- 方法名：get_project_name_cn
- 功能说明：
获取当前执行的流水线所属项目中文名称
- 输入参数：
无
- 返回：
类型：string

### 获取当前流水线ID

- 方法名：get_pipeline_id
- 功能说明：
获取当前执行的流水线ID
- 输入参数：
无
- 返回：
类型：string

### 获取当前流水线名称

- 方法名：get_pipeline_name
- 功能说明：
获取当前执行的流水线名称
- 输入参数：
无
- 返回：
类型：string

### 获取当前构建ID

- 方法名：get_pipeline_build_id
- 功能说明：
获取当前构建ID
- 输入参数：
无
- 返回：
类型：string

### 获取当前构建序号

- 方法名：get_pipeline_build_num
- 功能说明：
获取当前流水线第几次构建
- 输入参数：
无
- 返回：
类型：string

### 获取当前流水线启动类型

- 方法名：get_pipeline_start_type
- 功能说明：
获取当前流水线启动类型
- 输入参数：
无
- 返回：
类型：string

### 获取当前流水线启动用户ID

- 方法名：get_pipeline_start_user_id
- 功能说明：
获取当前流水线启动用户ID
- 输入参数：
无
- 返回：
类型：string

### 获取当前流水线启动用户名

- 方法名：get_pipeline_start_user_name
- 功能说明：
获取当前流水线启动用户名
- 输入参数：
无
- 返回：
类型：string

### 获取当前流水线启动时间

- 方法名：get_pipeline_time_start_mills
- 功能说明：
获取当前流水线启动时间（s）
- 输入参数：
无
- 返回：
类型：string

### 获取当前流水线版本

- 方法名：get_pipeline_version
- 功能说明：
获取当前流水线版本
- 输入参数：
无
- 返回：
类型：string

### 获取流水线创建人

- 方法名：get_pipeline_creator
- 功能说明：
获取流水线创建人
- 输入参数：
无
- 返回：
类型：string

### 获取流水线最近修改人

- 方法名：get_pipeline_modifier
- 功能说明：
获取流水线最近修改人
- 输入参数：
无
- 返回：
类型：string

### 获取插件私有设置

- 方法名：get_sensitive_conf
- 功能说明：
获取插件私有设置
- 输入参数：
私有设置字段名
- 返回：
类型：string

### 设置插件输出

- 方法名：set_output
- 功能说明：
设置插件执行结果和输出字段信息，供蓝盾agent处理
- 输入参数：
  - output
  - 类型：dict
  - 示例：
    ```json
    {
        "status": python_atom_sdk.status.SUCCESS,
        "message": "run succ",
        "type": python_atom_sdk.output_template_type.DEFAULT,
        "data": {
            "outputDemo": {
                "type": python_atom_sdk.output_field_type.STRING,
                "value": "test output"
            }
        }
    }
    ```
- 返回：
无

### 打印日志到控制台

- 方法名：log
- 功能说明：
打印日志到控制台，流水线执行时将收集控制台日志展示到流水线插件执行日志页面
- 示例：
```python
python_atom_sdk.log.debug("this is debug")        # 打印[DEBUG]: this is debug
python_atom_sdk.log.info("this is info")          # 打印[INFO]: this is info
python_atom_sdk.log.warning("this is warning")    # 打印[WARNING]: this is warning
python_atom_sdk.log.error("this is error")        # 打印[ERROR]: this is error
python_atom_sdk.log.critical("this is critical")  # 打印[CRITICAL]: this is critical
```

### 获取凭证

- 方法名：get_credential
- 功能说明：
根据凭证id，获取凭证详情
- 输入参数：

    参数名|是否必填|说明 | 备注
    ---|:--:|---:|:---
    credential_id | 是 | 凭证id | |

- 返回：tuple

字段名|是否必填|说明 | 备注
---|:--:|---:|:---
tuple[0] | 是 | 获取凭证是否成功 | true false |
tuple[1] | 是 | 凭证详情 | 格式为字典，不同类型的凭证key如下：<br>密码：password<br>用户名+密码：username、password<br>AccessToken：access_token<br>SecreKey：secretKey<br>AppId+SecreKey：appId、secretKey<br>SSH私钥：privateKey、passphrase<br>SSH私钥+私有token：token、privateKey、passphrase |
