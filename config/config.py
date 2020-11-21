# @Time    : 2020/11/21 8:38 下午
# @Author  : h0rs3fa11
# @FileName: config.py
# @Software: PyCharm
import redis
import logging


class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@127.0.0.1:3307/user_manager"

    SECRET_KEY = 'e\x94I\xe0\xb2L\xab\x01\xcf"\xc5\xe1j=\xf4\xcb\xc2\x8a\xfd\x14\xe13JZ'

    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    SESSION_TYPE = 'redis'
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    PERMANENT_SESSION_LIFETIME = 24 * 60 * 60

    LOG_LEVEL = logging.DEBUG


class DevelopementConfig(Config):
    pass


class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = logging.ERROR


class UnittestConfig(Config):
    TESTING = True


configs = {
    "development": DevelopementConfig,
    "production": ProductionConfig,
    "test": UnittestConfig,
}
