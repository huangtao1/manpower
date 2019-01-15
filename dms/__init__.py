#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by huangtao@oraro
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import config

mail = Mail()
db = SQLAlchemy()
# 这样就使未登录的直接跳转到登录界面
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    # 注册每个APP view对应的蓝本
    # 处理根url
    from dms.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    # 登录
    from dms.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    # 管理
    from dms.manager import manager as manager_blueprint
    app.register_blueprint(manager_blueprint, url_prefix='/manager')
    return app
