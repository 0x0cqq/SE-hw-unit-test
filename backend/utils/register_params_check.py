# -*- coding: utf-8 -*-

import re

# username: 必填，用户账号
# password: 必填，用户密码
# nickname: 必填，用户昵称
# mobile: 必填，手机号
# url: 必填，用户个人地址链接
# magic_number: 选填，用户喜欢的幸运数字


# 参数要求：
# 用户账号为长度 5-12 的字母串加数字，且必须包含这两种类型，所有字母串必须在数字前面，大写字母和小写字母均合法
# 用户密码为长度 8-15 的字符串，由大写、小写字母、数字和标点符号组成且必须包含这四种类型，有效的标点符号为-_*^
# 用户的手机号的格式为+[区号].[手机号]，其中区号必须为两位数字，手机号必须为 12 位数字，例如+12.123456789012
# 用户的个人地址链接包含协议和域名两部分
#   协议部分必须为 http:// 或者 https://
#   域名部分包含 1 到多个点 .，表示以点 . 分隔的标签序列，且总长度不超过 48 个字符（包含 .）。标签序列只能由下列字符组成：
#       大小写字母 A 到 Z 和 a 到 z
#       数字 0 到 9，但最后一段顶级域名不能是纯数字（如 163.com 可以但 163.126 不可以）
#       连字符-，但不能作为首尾字符
# magic_number为非负数 int 数值，可选参数（在设计测试用例时无需考虑最大值上界）

# 返回值要求：
#   返回错误或缺失字段名（如有多个只需要按前述顺序返回第一个）以及一个 bool 值表示是否出错，这表示你需要按上述顺序依次检查每一个字段是否缺失或错误
#   如果正确，返回 "ok" 以及 True
#   如果 magic_number 缺失，请为 content 添加默认值为 0 的 magic_number 字段

def register_params_check(content: dict):

    # 用户账号为长度 5-12 的字母串加数字，且必须包含这两种类型，所有字母串必须在数字前面，大写字母和小写字母均合法
    if "username" not in content:
        return "username", False
    username = content["username"]
    if not isinstance(username, str) or len(username) < 5 or len(username) > 12:
        return "username", False
    if not re.match(r"^[a-zA-Z]+[0-9]+$", username):
        return "username", False

    # 用户密码为长度 8-15 的字符串，由大写、小写字母、数字和标点符号组成且必须包含这四种类型，有效的标点符号为-_*^
    if "password" not in content:
        return "password", False
    password = content["password"]
    if not isinstance(password, str) or len(password) < 8 or len(password) > 15:
        return "password", False
    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[-_*^])[a-zA-Z\d\-_*^]+$", password):
        return "password", False

    # 用户的手机号的格式为+[区号].[手机号]，其中区号必须为两位数字，手机号必须为 12 位数字，例如+12.123456789012
    if "mobile" not in content:
        return "mobile", False
    mobile = content["mobile"]
    if not isinstance(mobile, str):
        return "mobile", False
    if not re.match(r"^\+\d{2}\.\d{12}$", mobile):
        return "mobile", False

    # 昵称必须存在
    if "nickname" not in content:
        return "nickname", False
    nickname = content["nickname"]
    if not isinstance(nickname, str):
        return "nickname", False

    # 用户的个人地址链接包含协议和域名两部分
    if "url" not in content:
        return "url", False
    url = content["url"]
    if not isinstance(url, str):
        return "url", False
    # 协议部分必须为 http:// 或者 https://
    if not re.match(r"^https?://", url):
        return "url", False
    # 提取域名部分
    domain = re.match(
        r"^https?://(([a-zA-Z0-9\-]{1,48}\.)*[a-zA-Z0-9\-]{1,48})$", url).group(1)
    # 用 . 分割域名
    domain_list = domain.split(".")
    # 标签不能用 - 开头或结尾
    for tag in domain_list:
        if tag.startswith("-") or tag.endswith("-"):
            return "url", False
    # 最后一个标签不能为纯数字
    if domain_list[-1].isdigit():
        return "url", False

    # magic_number为非负数 int 数值，可选参数（在设计测试用例时无需考虑最大值上界）
    if "magic_number" not in content:
        content["magic_number"] = 0
    magic_number = content["magic_number"]
    if int(magic_number) < 0:
        return "magic_number", False

    return "ok", True
