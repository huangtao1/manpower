#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by mark.huang on 2018/6/7.
from . import auth  # blueprint need
from flask_login import login_user, logout_user, login_required, current_user
from ldap3 import Server, Connection, ALL
from flask import render_template, redirect, url_for, request, current_app, flash, session
from config import Config
from .models import User, Role, Menu
from datetime import datetime
from dms import db
import base64


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    登录模块
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_base = base64.b64encode(password.encode('utf-8'))
        # 调用ldap进行登录认证,因为部分用户简历在dc=oraro,dc=com下面所以要做不同的处理
        try:
            conn = Connection(Config.LDAP_HOST, 'cn=%s,dc=oraro,dc=com' % username, password, auto_bind=True)
            # 如果是第一次登录就往数据库写入user数据,否则只更新last seen的值
            user = User.query.filter(User.username == username).first()
            if user is not None:
                if user.active:
                    user.last_seen = datetime.now()
                    user.password_hash = user.pass_exchange(password)
                    db.session.add(user)
                    db.session.commit()
                    login_user(user, True)
                    role = user.role
                    if role and role.menu:
                        menu_ids = [menu_id for menu_id in role.menu.split(',') if id]
                        menus = [menu for menu in Menu.query.filter(
                            db.and_(Menu.active == True,
                                    Menu.id.in_(menu_ids))).order_by(Menu.menu_order).all()]
                    else:
                        menus = []
                    # 添加session
                    session['user'] = {'username': user.username, 'password': password_base,
                                       'display_name': user.display_name,
                                       'email': user.email,
                                       'role': user.role.name, 'id': user.id, 'avatar': user.gravatar()}
                    session['menu'] = create_menu(menus)
                    session['index_page'] = user.role.index_page

                    return redirect(request.args.get('next') or url_for(user.role.index_page))
                else:
                    flash('账号处于未激活状态,请联系管理员!!!', 'warning')
                    return redirect(url_for('auth.login'))
            else:
                user = User()
                user.username = username
                user.password_hash = user.pass_exchange(password)
                user.email = username + Config.MAIL_TAIL
                user.display_name = username
                user.active = True
                user.member_since = datetime.now()
                user.last_seen = datetime.now()
                # 初始化一个角色,后面管理员再去改
                role = Role.query.filter(Role.name == 'admin').first()
                user.role = role
                db.session.add(user)
                db.session.commit()
                login_user(user, True)
                role = user.role
                if role and role.menu:
                    menu_ids = [menu_id for menu_id in role.menu.split(',') if id]
                    menus = [menu for menu in Menu.query.filter(
                        db.and_(Menu.active == True,
                                Menu.id.in_(menu_ids))).order_by(Menu.menu_order).all()]
                else:
                    menus = []
                # 添加session
                session['user'] = {'username': user.username, 'password': password_base,
                                   'display_name': user.display_name,
                                   'email': user.email,
                                   'role': user.role.name, 'id': user.id, 'avatar': user.gravatar()}
                session['menu'] = create_menu(menus)
                session['index_page'] = user.role.index_page

                return redirect(request.args.get('next') or url_for(user.role.index_page))
        except Exception as e:
            print(e)
            try:
                conn = Connection(Config.LDAP_HOST, 'cn=%s,' % username + Config.LDAP_SEARCH_BASE, password,
                                  auto_bind=True)
                # 如果是第一次登录就往数据库写入user数据,否则只更新last seen的值
                user = User.query.filter(User.username == username).first()
                if user is not None:
                    if user.active:
                        user.last_seen = datetime.now()
                        user.password_hash = user.pass_exchange(password)
                        db.session.add(user)
                        db.session.commit()
                        login_user(user, True)
                        role = user.role
                        if role and role.menu:
                            menu_ids = [menu_id for menu_id in role.menu.split(',') if id]
                            menus = [menu for menu in Menu.query.filter(
                                db.and_(Menu.active == True,
                                        Menu.id.in_(menu_ids))).order_by(Menu.menu_order).all()]
                        else:
                            menus = []
                        # 添加session
                        session['user'] = {'username': user.username, 'password': password_base,
                                           'display_name': user.display_name,
                                           'email': user.email,
                                           'role': user.role.name, 'id': user.id, 'avatar': user.gravatar()}
                        session['menu'] = create_menu(menus)
                        session['index_page'] = user.role.index_page

                        return redirect(request.args.get('next') or url_for(user.role.index_page))
                    else:
                        flash('账号处于未激活状态,请联系管理员!!!', 'warning')
                        return redirect(url_for('auth.login'))
                else:
                    user = User()
                    user.username = username
                    user.password_hash = user.pass_exchange(password)
                    user.email = username + Config.MAIL_TAIL
                    user.display_name = username
                    user.active = True
                    user.member_since = datetime.now()
                    user.last_seen = datetime.now()
                    # 初始化一个角色,后面管理员再去改
                    role = Role.query.filter(Role.name == 'admin').first()
                    user.role = role
                    db.session.add(user)
                    db.session.commit()
                    login_user(user, True)
                    role = user.role
                    if role and role.menu:
                        menu_ids = [menu_id for menu_id in role.menu.split(',') if id]
                        menus = [menu for menu in Menu.query.filter(
                            db.and_(Menu.active == True,
                                    Menu.id.in_(menu_ids))).order_by(Menu.menu_order).all()]
                    else:
                        menus = []
                    # 添加session
                    session['user'] = {'username': user.username, 'password': password_base,
                                       'display_name': user.display_name,
                                       'email': user.email,
                                       'role': user.role.name, 'id': user.id, 'avatar': user.gravatar()}
                    session['menu'] = create_menu(menus)
                    session['index_page'] = user.role.index_page

                    return redirect(request.args.get('next') or url_for(user.role.index_page))
            except Exception as e:
                print(e)
                flash('用户名或密码错误!', 'danger')
                return redirect(url_for('auth.login'))

    else:
        return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():
    """用户登出"""

    logout_user()
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    用户信息修改
    """
    if request.method == "POST":
        user = User.query.filter(User.username == session['user']['username']).first()
        nickname = request.form.get('nickname')
        user.display_name = nickname
        db.session.add(user)
        db.session.commit()
        session['user']['display_name'] = nickname
        flash('个人信息修改成功!!', 'success')
    return render_template('auth/profile.html', user=current_user)


@auth.route('/lock_screen',methods=['POST','GET'])
@login_required
def lock_screen():
    """
    用户锁定
    """
    return render_template('auth/lock.html')


def create_menu(menus):
    """创建默认菜单"""

    parents = []
    for menu in menus:
        if not menu.parent_id:
            parents.append({'id': menu.id, 'name': menu.menu_name, 'url': menu.menu_url, 'style': menu.menu_icon,
                            'children': []})

    for menu in menus:
        if menu.parent_id:
            for parent in parents:
                if parent['id'] == menu.parent_id:
                    parent['children'].append({'id': menu.id, 'name': menu.menu_name, 'url': menu.menu_url,
                                               'style': menu.menu_icon, 'children': []})
    return parents
