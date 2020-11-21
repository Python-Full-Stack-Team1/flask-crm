# @Time    : 2020/11/21 8:20 下午
# @Author  : h0rs3fa11
# @FileName: __init__.py.py
# @Software: PyCharm
import redis
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from api.utils.log_utils import setup_log
from config.config import configs, Config

db = SQLAlchemy()
redis_store = None


def create_app(config_name):
    # 根据config选项加载不同配置
    config = configs[config_name]
    # 设置日志级别
    setup_log(config_name)

    # app加载config配置
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    # redis设置
    global redis_store
    redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)

    Session(app)

    # 蓝图注册
    from api.auth import auth_blu
    app.register_blueprint(auth_blu)

    from api.profile import profile_blu
    app.register_blueprint(profile_blu)

    from api.passport import pass_blu
    app.register_blueprint(pass_blu)

    from api.session_profile import sprofile_blu
    app.register_blueprint(sprofile_blu)

    return app
