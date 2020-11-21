# @Time    : 2020/11/21 8:44 下午
# @Author  : h0rs3fa11
# @FileName: log_utils.py
# @Software: PyCharm
import logging
from logging.handlers import RotatingFileHandler
from config.config import configs


def setup_log(config_name):
    logging.basicConfig(level=configs[config_name].LOG_LEVEL)
    file_log_handler = RotatingFileHandler('logs/log', maxBytes=1024 * 1024 * 100, backupCount=10)
    formator = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    file_log_handler.setFormatter(formator)
    logging.getLogger().addHandler(file_log_handler)
