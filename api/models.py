# @Time    : 2020/11/21 8:36 下午
# @Author  : h0rs3fa11
# @FileName: models.py
# @Software: PyCharm
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


# 基础表，包含创建时间和更新时间
class BaseModel:
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())


# 用户登录信息表
class UserLogin(BaseModel, db.Model):
    __tablename__ = 'user_login'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.id'))
    mobile = db.Column(db.String(16), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    last_login = db.Column(db.DateTime, default=datetime.now)

    @property
    def password(self):
        raise AttributeError('当前属性不可读')

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    @staticmethod
    def crypto_secret(value):
        return generate_password_hash(value)

    def check_password(self, value):
        return check_password_hash(self.password_hash, value)

    def to_dict(self):
        res_dict = {
            'mobile': self.mobile,
        }

        return res_dict


# 用户信息/资料表
class UserInfo(BaseModel, db.Model):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mobile = db.Column(db.String(16), unique=True, nullable=False)
    nickname = db.Column(db.String(10), unique=True)
    avatar_url = db.Column(db.String(50))
    signature = db.Column(db.String(60))
    sex = db.Column(db.Enum('0', '1', '2'), default='0')
    birth_date = db.Column(db.DateTime)

    def to_dict(self):
        res_dict = {
            'mobile': self.mobile,
            'nickname': self.nickname,
            'avatar_url': self.avatar_url,
            'signature': self.signature,
            'sex': self.sex,
            'birth_date': self.birth_date
        }
        return res_dict

    def from_dict(self, res_dict):
        if res_dict['mobile']: self.mobile = res_dict['mobile']
        if res_dict['nickname']: self.nickname = res_dict['nickname']
        if res_dict['avatar_url']: self.avatar_url = res_dict['avatar_url']
        if res_dict['signature']: self.signature = res_dict['signature']
        if res_dict['sex']: self.sex = res_dict['sex']
        if res_dict['birth_date']: self.birth_date = res_dict['birth_date']
