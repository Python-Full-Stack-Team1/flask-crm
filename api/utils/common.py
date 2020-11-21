# @Time    : 2020/11/15 8:24 下午
# @Author  : h0rs3fa11
# @FileName: common.py
# @Software: PyCharm
from functools import wraps
from api import redis_store
from flask import session, current_app, g, request
from api.models import UserInfo
from api.utils.auth_helper import Auth
from api.utils.response_utils import error, HttpCode


def verify_imgcode(img_code_id, img_code):
    redis_img_code = None
    try:
        redis_img_code = redis_store.get(f'img_data:{img_code_id}')
    except Exception as e:
        current_app.logger.error(e)

    if not redis_img_code:
        return -2

    if img_code.lower() != redis_img_code.lower():
        return -1

    return 0


def user_login_data(view_func):
    def wrapper(*args, **kwargs):
        user_id = session.get('user_id')

        user = None
        if user_id:
            try:
                from api.models import UserInfo
                user = UserInfo.query.get(user_id)
            except Exception as e:
                current_app.logger.error(e)
        g.user = user

        return view_func(*args, **kwargs)

    return wrapper

def auth_identify(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        result = Auth().identify(request)
        if result['code'] == 200:
            user_id = result['data']['user_id']
            g.user = UserInfo.query.get(user_id)

            return view_func(*args, **kwargs)

        else:
            return error(HttpCode.auth_error, "用户未通过认证")

    return wrapper