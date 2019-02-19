#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by mark.huang on 2018/6/8.
import hashlib
from flask_login import UserMixin
from datetime import datetime
from omp import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash  # 密码加密
from flask import request


class User(UserMixin, db.Model):
    """
    用户表
    """
    __tablename__ = 'omp_user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(128), unique=True, index=True)
    display_name = db.Column(db.String(64), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('omp_role.id'))
    role = db.relationship('Role', backref=db.backref('user', order_by=id))
    organize_id = db.Column(db.Integer, db.ForeignKey('omp_organization.id'))
    organize = db.relationship('Organization', backref=db.backref('user', order_by=id))
    password_hash = db.Column(db.String(128))
    location = db.Column(db.String(64))
    member_since = db.Column(db.DateTime(), default=datetime.now())
    last_seen = db.Column(db.DateTime(), default=datetime.now())
    active = db.Column(db.Boolean, default=True)
    real_avatar = db.Column(db.String(128))
    rank = db.Column(db.String(128))

    def __repr__(self):
        return '<User %r>' % self.username

    def __getitem__(self, item):
        return getattr(self, item)

    def pass_check(self, pass_hash, password):
        return check_password_hash(pass_hash, password)

    def pass_exchange(self, password):
        return generate_password_hash(password)

    def get_mail_hash(self):
        self.real_avatar = hashlib.md5(self.email.encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.real_avatar or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)


# 登录必须要加载此装饰器
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Role(db.Model):
    """
    角色表
    """
    __tablename__ = 'omp_role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    index_page = db.Column(db.String(64))
    menu = db.Column(db.String(200))

    def __repr__(self):
        return '<Role %r>' % self.name

    def __getitem__(self, item):
        return getattr(self, item)


class SystemParameter(db.Model):
    """系统参数表"""

    __tablename__ = 'omp_parameter'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64))
    value = db.Column(db.Text)
    flag = db.Column(db.Boolean, default=True)
    note = db.Column(db.String(255))

    def __repr__(self):
        return '<SystemParameter %r>' % self.key

    def __getitem__(self, item):
        return getattr(self, item)


class Menu(db.Model):
    """菜单"""
    __tablename__ = 'omp_menu'

    id = db.Column(db.Integer, primary_key=True)
    menu_name = db.Column(db.String(64))
    menu_url = db.Column(db.String(64))
    menu_icon = db.Column(db.String(64))
    menu_order = db.Column(db.Integer)
    menu_desc = db.Column(db.String(64))
    active = db.Column(db.Boolean, default=True)
    is_parent = db.Column(db.Boolean, default=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('omp_menu.id'), nullable=True)
    parent = db.relation('Menu', uselist=False, remote_side=[id],
                         backref=db.backref('children', order_by=menu_order))

    def __repr__(self):
        return '<Menu %s>' % self.menu_name


class Organization(db.Model):
    """
    组织架构表
    """
    __tablename__ = 'omp_organization'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    is_parent = db.Column(db.Boolean, default=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('omp_organization.id'), nullable=True)
    parent = db.relation('Organization', uselist=False, remote_side=[id], backref=db.backref('children'))

    def __repr__(self):
        return '<Organization %s>' % self.name

    def __getitem__(self, item):
        return getattr(self, item)
