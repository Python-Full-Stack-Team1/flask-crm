# @Time    : 2020/11/15 8:24 下午
# @Author  : h0rs3fa11
# @FileName: common.py
# @Software: PyCharm
from flask import current_app
from api import redis_store


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
