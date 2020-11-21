# @Time    : 2020/11/21 10:57 下午
# @Author  : h0rs3fa11
# @FileName: auth_helper.py
# @Software: PyCharm
import datetime
import jwt
import time
from config.config import configs
from api.models import UserLogin
from api.utils.response_utils import success, error, HttpCode


class Auth:
    @staticmethod
    def encode_auth_token(user_id, login_time):
        """
        生成认证token
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'iss': 'test',
                'data': {
                    'id': user_id,
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                configs.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, configs.SECRET_KEY, leeway=datetime.timedelta(days=1))
            # 取消过期时间验证
            # payload = jwt.decode(auth_token, Config.SECRET_KEY, options={'verify_exp': False})
            if 'data' in payload and 'id' in payload['data']:
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'

    def authenticate(self, mobile, password):
        user = UserLogin.query.filter_by(mobile=mobile).first
        if not user:
            return error(HttpCode.auth_error, '用户不存在')
        if user.check_password(password):
            login_time = int(time.time())
            user.last_login = login_time
            user.update()

            token = self.encode_auth_token(user.id, login_time)
            token = str(token, encoding='utf-8')
            return success('登录成功', data={'token': token})
        else:
            return error(HttpCode.params_error, '密码错误')

    def identify(self, request):
        """
        用户鉴权
        :param request:
        :return:
        """
        # 获取header中的Authorization
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token_arr = auth_header.split(" ")
            if not auth_token_arr or auth_token_arr[0] != 'JWT' or len(auth_token_arr) != 2:
                return HttpCode.auth_error
            else:
                auth_token = auth_token_arr[1]
                payload = self.decode_auth_token(auth_token)
                if not isinstance(payload, str):
                    user_id = payload.get('data').get('id')
                    login_time = payload.get('data').get('login_time')
                    user = UserLogin.query.get(user_id)
                    if not user:
                        return HttpCode.un_auth_error
                    else:
                        if user.last_login == login_time:
                            return success(msg='用户认证成功', data={"user_id": user.user_id})
                        else:
                            return error(code=HttpCode.auth_error, msg='用户认证失败')
                else:
                    return error(code=HttpCode.auth_error, msg='用户认证失败')
        else:
            return error(code=HttpCode.auth_error, msg='用户认证失败')
