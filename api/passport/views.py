# @Time    : 2020/11/10 9:41 下午
# @Author  : h0rs3fa11
# @FileName: view.py
# @Software: PyCharm
from flask_restful import Resource, reqparse, inputs
from datetime import datetime as dt
from api import db, redis_store
from api.utils.common import verify_imgcode
from api.utils.constants import IMAGE_CODE_REDIS_EXPIRES
from flask import current_app, session, make_response
from api.models import UserLogin, UserInfo
from api.utils.response_utils import success, error, HttpCode
from api.thirdparty.captcha import captcha


class LoginView(Resource):
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('mobile', type=inputs.regex('1[3456789]\\d{9}'), required=True,
                            nullable=False, location=['json'], help='手机号参数不正确')
        parser.add_argument('password', required=True, nullable=False, location=['json'],
                            help='密码参数不正确')
        args = parser.parse_args()

        verify_code = verify_imgcode(args.img_code_id, args.img_code)
        if verify_code == -2:
            return error(HttpCode.params_error, '验证码id不正确', {'img_code_id': args.img_code_id})
        elif verify_code == -1:
            return error(HttpCode.params_error, '验证码不正确', {'img_code': args.img_code})

        try:
            user = UserLogin.query.filter(UserLogin.mobile == mobile).first()
        except Exception as e:
            current_app.logger.error(e)
            return error(HttpCode.db_error, msg='获取数据出错')

        if not user:
            return error(HttpCode.params_error, msg='用户不存在')

        if not user.check_password(args.password):
            return error(HttpCode.params_error, msg='密码错误')

        # 保存session
        session['user_id'] = user.id
        session['mobile'] = args.mobile

        user.last_login = dt.now()

        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return error(HttpCode.db_error, msg='添加数据失败')

        return success(msg='登录成功', data=user.to_dict())


class RegisterView(Resource):
    def post(self):
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

        # 验证码
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


class LogoutView(Resource):
    def post(self):
        session.pop('user_id', '')
        session.pop('mobile', '')
        return success('登出成功')


class ImageCodeView(Resource):
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('cur_id', required=True, nullable=False, location=['json'],
                            help='验证码图片id参数不正确')
        parser.add_argument('pre_id', required=True, nullable=False, location=['json'],
                            help='验证码图片id参数不正确')
        args = parser.parse_args()

        name, text, img_data = captcha.captcha.generate_captcha()
        try:
            redis_store.set(f'img_data:{arg.cur_id}', text, IMAGE_CODE_REDIS_EXPIRES)
            if args.pre_id:
                redis_store.delete(f'img_data:{args.pre_id}')
        except Exception as e:
            current_app.logger.error(e)
            return error(code=HttpCode.db_error, msg='redis存储失败')

        response = make_response(img_data)
        response.headers['Content-Type'] = 'image/jpg'

        return response
