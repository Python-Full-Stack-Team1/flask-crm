# @Time    : 2020/11/21 9:25 下午
# @Author  : h0rs3fa11
# @FileName: response_utils.py
# @Software: PyCharm
from flask import jsonify


class HttpCode:
    ok = 200
    params_error = 400
    server_error = 500
    auth_error = 401
    db_error = 777


def rep_result(code, msg, data):
    return jsonify(code=code, msg=msg, data=data or {})


def success(msg, data=None):
    return rep_result(HttpCode.ok, msg, data)


def error(code, msg, data=None):
    return rep_result(code, msg, data)
