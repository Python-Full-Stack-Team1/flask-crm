# @Time    : 2020/11/21 8:57 下午
# @Author  : h0rs3fa11
# @FileName: __init__.py.py
# @Software: PyCharm
from flask_restful import Api
from flask import Blueprint
from api.profile.views import InfoView, AvatarView

profile_blu = Blueprint('profile', __name__, url_prefix='/profile')

api = Api(profile_blu)

api.add_resource(InfoView, '/info')
api.add_resource(AvatarView, '/avatar')
