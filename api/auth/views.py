# @Time    : 2020/11/21 8:58 下午
# @Author  : h0rs3fa11
# @FileName: views.py
# @Software: PyCharm
from flask_restful import Resource, reqparse, inputs
from flask import current_app
from api.utils.common import verify_imgcode
from api.utils.response_utils import error, success, HttpCode
from api.models import UserInfo, UserLogin
from api import db


class LoginView(Resource):
    def post(self):
        return ('auth/ login')


class RegisterView(Resource):
    def post(self):
        # 参数校验
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('mobile', type=inputs.regex('1[3456789]\\d{9}'), required=True,
                            nullable=False, location=['json'], help='手机号参数不正确')
        parser.add_argument('nickname', type=inputs.regex('^[A-Za-z][A-Za-z0-9]{2,7}'), required=True,
                            nullable=False, location=['json'], help='昵称格式不正确')
        parser.add_argument('password', required=True, nullable=False, location=['json'],
                            help='密码参数不正确')
        parser.add_argument('img_code_id', required=True, nullable=False, location=['json'],
                            help='验证码图片id参数不正确')
        parser.add_argument('img_code', required=True, nullable=False, location=['json'],
                            help='验证码参数不正确')

        args = parser.parse_args()
        # 验证码校验
        verify_code = verify_imgcode(args.img_code_id, args.img_code)
        if verify_code == -2:
            return error(HttpCode.params_error, '验证码id不正确', {'img_code_id': args.img_code_id})
        elif verify_code == -1:
            return error(HttpCode.params_error, '验证码不正确', {'img_code': args.img_code})

        user_profile = UserInfo()
        user_profile.nickname = args.nickname
        user_profile.mobile = args.mobile

        try:
            db.session.add(user_profile)
            db.session.commit()
            userinfo = UserInfo.query.filter(UserInfo.mobile == args.mobile).first()
            if not userinfo:
                return error(code=HttpCode.db_error, msg='添加数据失败')

        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return error(code=HttpCode.db_error, msg='添加数据失败')

        user = UserLogin()
        user.mobile = args.mobile
        user.password_hash = user.crypto_secret(args.password)
        user.user_id = user_profile.id

        try:
            db.session.add(user)
            db.session.add(user_profile)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            return error(code=HttpCode.db_error, msg='注册失败', data=user.to_dict())

        return success(msg='注册成功', data=user.to_dict())


class ImageCodeView(Resource):
    def post(self):
        return ('auth /imgcode')
