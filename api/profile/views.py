# @Time    : 2020/11/21 8:58 下午
# @Author  : h0rs3fa11
# @FileName: views.py
# @Software: PyCharm
from flask_restful import Resource

class InfoView(Resource):
    def post(self):
        return 'profile/ info'

class AvatarView(Resource):
    def post(self):
        return 'profile/ avatar'