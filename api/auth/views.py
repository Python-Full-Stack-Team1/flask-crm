# @Time    : 2020/11/21 8:58 下午
# @Author  : h0rs3fa11
# @FileName: views.py
# @Software: PyCharm
from flask_restful import Resource, reqparse, inputs
from api.utils.auth_helper import Auth


class LoginView(Resource):
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('mobile', type=inputs.regex('1[3456789]\\d{9}'), required=True,
                            nullable=False, location=['json'], help='手机号参数不正确')
        parser.add_argument('password', required=True, nullable=False, location=['json'],
                            help='密码参数不正确')
        args = parser.parse_args()

        Auth().authenticate(args.mobile, args.password)
