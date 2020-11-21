# @Time    : 2020/11/21 11:20 下午
# @Author  : h0rs3fa11
# @FileName: __init__.py.py
# @Software: PyCharm
from flask import Blueprint
from flask_restful import Api
from api.passport.views import LoginView, RegisterView, ImageCodeView

pass_blu = Blueprint('auth', __name__, url_prefix='/passport')

api = Api(pass_blu)
api.add_resource(LoginView, '/login')
api.add_resource(RegisterView, '/register')
api.add_resource(ImageCodeView, '/imagecode')
