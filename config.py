#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by mark.huang on 2018/6/7.
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    BASEDIR = basedir
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'opts@2018!#$@@@!$!stpo'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[OPTS]'
    FLASKY_MAIL_SENDER = 'OPTS Admin <opts@oraro.net>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    MAIL_SERVER = 'smtp.263.com'
    MAIL_PORT = 587
    MAIL_USER_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_TAIL = '@oraro.net'
    DB_NAME = os.environ.get('DB_NAME') or 'opts'
    DB_HOST = os.environ.get('DB_HOST') or '192.168.9.224'
    DB_USERNAME = os.environ.get('DB_USERNAME') or 'root'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'Aa123456'
    # 生产环境
    PRO_DB_NAME = os.environ.get('DB_NAME') or 'opts'
    PRO_DB_HOST = os.environ.get('DB_HOST') or '192.168.8.240'
    PRO_DB_USERNAME = os.environ.get('DB_USERNAME') or 'root'
    PRO_DB_PASSWORD = os.environ.get('DB_PASSWORD') or '123456'
    UTIL_FOLDER = os.path.join(basedir, 'opts/utils')
    # ldap config
    LDAP_HOST = '192.168.8.10'
    LDAP_PORT = '389'
    LDAP_ADMIN_USER = 'cn=admin,dc=oraro,dc=com'
    LDAP_PASSWD = 'oraro@123456'
    LDAP_SEARCH_BASE = 'ou=User,dc=oraro,dc=com'
    @staticmethod
    def init_app(app):
        pass


# 开发环境
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'mysql://{0}:{1}@{2}:3306/{3}?charset=utf8'.format(Config.DB_USERNAME, Config.DB_PASSWORD,
                                                                                 Config.DB_HOST, Config.DB_NAME)

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        # 配置日志文件
        import logging
        import datetime
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(name)s[line:%(lineno)d]:%(levelname)s %(message)s',
        )

        # 输出到文件
        log_file = os.path.join(basedir, 'logs', datetime.datetime.now().strftime('%Y-%m-%d'), 'opts.log')
        if not os.path.exists(os.path.dirname(log_file)):
            os.makedirs(os.path.dirname(log_file))

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

        # 输出到控制台
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(console_handler)


# 测试环境
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'mysql://{0}:{1}@{2}:3306/{3}?charset=utf8'.format(Config.DB_USERNAME, Config.DB_PASSWORD,
                                                                                 Config.DB_HOST, Config.DB_NAME)

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


# 生产环境
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'mysql://{0}:{1}@{2}:3306/{3}?charset=utf8'.format(Config.PRO_DB_USERNAME,
                                                                                 Config.PRO_DB_PASSWORD,
                                                                                 Config.PRO_DB_HOST, Config.PRO_DB_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        # 配置日志文件
        import logging
        import datetime

        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(name)s[line:%(lineno)d]:%(levelname)s %(message)s',
        )

        # 输出到文件
        log_file = os.path.join(basedir, 'logs', datetime.datetime.now().strftime('%Y-%m-%d'), 'opts.log')
        if not os.path.exists(os.path.dirname(log_file)):
            os.makedirs(os.path.dirname(log_file))

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

        # 输出到控制台
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(console_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
