# @Time    : 2020/11/21 8:58 下午
# @Author  : h0rs3fa11
# @FileName: views.py
# @Software: PyCharm
from flask_restful import Resource

class LoginView(Resource):
    def post(self):
        return('auth/ login')

class RegisterView(Resource):
    def post(self):
        return('auth/ register')

class ImageCodeView(Resource):
    def post(self):
        return('auth /imgcode')