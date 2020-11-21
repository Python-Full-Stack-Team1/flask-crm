# @Time    : 2020/11/21 8:58 下午
# @Author  : h0rs3fa11
# @FileName: views.py
# @Software: PyCharm
import re
from flask_restful import Resource
from api.models import UserLogin, UserInfo
from flask import request, session, current_app, g
from api.utils.response_utils import success, error, HttpCode
from api.utils.constants import QINIU_DOMIN_PREFIX
from api.thirdparty import image_storage
from api.utils.common import auth_identify
from api import db


class InfoView(Resource):
    @auth_identify
    def post(self):
        user_profile = {}
        dict_data = request.args
        user_profile['mobile'] = dict_data.get('mobile')
        user_profile['nickname'] = dict_data.get('nickname')
        # user_profile['avatar_url'] = dict_data.get('avatar_url')
        user_profile['signature'] = dict_data.get('signature')
        user_profile['sex'] = dict_data.get('sex')
        user_profile['birth_date'] = dict_data.get('birth_date')

        if not all(user_profile.values()):
            return error(HttpCode.params_error, '参数不能全为空')

        if user_profile['mobile'] and not re.fullmatch(r'1[356789]\d{9}', user_profile['mobile']):
            return error(HttpCode.params_error, msg='手机号格式错误')

        if user_profile['nickname'] and not re.fullmatch(r'^[A-Za-z][A-Za-z0-9]{2,7}', user_profile['nickname']):
            return error(HttpCode.params_error, msg='昵称格式错误')

        if user_profile['sex'] and user_profile['sex'] not in ['0', '1', '2']:
            return error(HttpCode.params_error, msg='性别输入错误')

        try:
            user = UserInfo.query.filter(UserInfo.id == user_id).first()
        except Exception as e:
            current_app.logger.error(e)
            return error(HttpCode.db_error, '获取数据失败')

        if not user:
            return error(HttpCode.params_error, '用户不存在')

        user.from_dict(user_profile)

        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return error(HttpCode.db_error, '更新数据失败')

        return success('修改成功')


class PasswordView(Resource):
    @auth_identify
    def post(self):
        dict_data = request.args
        old_password = dict_data.get('old_password')
        new_password = dict_data.get('new_password')

        # session鉴权
        user_id = session.get('user_id')
        if not user_id:
            return error(HttpCode.params_error, '请先登录')

        try:
            user = UserLogin.query.filter(UserLogin.id == user_id).first()
        except Exception as e:
            current_app.logger.error(e)
            return error(HttpCode.params_error, '查询失败')

        if not user:
            return error(HttpCode.params_error, '用户不存在')

        if not user.check_password(old_password):
            return error(HttpCode.params_error, '旧密码不符')

        user.password_hash = UserLogin.crypto_secret(new_password)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return error(HttpCode.db_error, '添加数据失败')

        return success('修改成功')


class AvatarView(Resource):
    @auth_identify
    def post(self):
        file_avatar = request.args.get('avatar')

        if not file_avatar:
            return error(HttpCode.params_error, '对象不存在')

        try:
            img_data = file_avatar.read()
            image_name = image_storage.image_storage(img_data)
        except Exception as e:
            current_app.logger.error(e)
            return error(HttpCode.params_error, '上传失败')

        g.user.avatar_url = QINIU_DOMIN_PREFIX + image_name

        return success(msg='上传成功', data={'avatar_url': QINIU_DOMIN_PREFIX + image_name})
