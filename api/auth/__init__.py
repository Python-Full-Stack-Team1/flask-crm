# @Time    : 2020/11/21 8:57 下午
# @Author  : h0rs3fa11
# @FileName: __init__.py.py
# @Software: PyCharm
from flask import Blueprint
from flask_restful import Api
from api.auth.views import LoginView

auth_blu = Blueprint('auth', __name__, url_prefix='/auth')

api = Api(auth_blu)
api.add_resource(LoginView, '/login')