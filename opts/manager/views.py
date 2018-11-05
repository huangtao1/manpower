#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by mark.huang on 2018/7/2.
from . import manager
from flask_login import login_required, current_user
from flask import redirect, url_for, render_template, request, flash, session
from opts.auth.models import SystemParameter, Menu, Role, User, Organization
from opts import db
from opts.auth.views import create_menu
from ldap3 import Server, Connection, ALL
from config import Config


@manager.route('/accounts_manage')
@login_required
def accounts_manage():
    """
    账号管理
    :return:
    """
    # 查询所有用户
    users = User.query.all()
    return render_template('manager/accounts.html', users=users)


@manager.route('/show_menus')
@login_required
def show_menus():
    """
    展示菜单
    :return:
    """
    menus = Menu.query.order_by(Menu.menu_order).all()
    parents = []
    result = {}
    for menu in menus:
        if menu.parent and menu.parent in result.keys():
            result[menu.parent].append(menu)
        elif menu.parent:
            result.update({menu.parent: [menu]})
            if not menu.parent in parents:
                parents.append(menu.parent)
        else:
            if not menu in parents:
                parents.append(menu)
            result.update({menu.parent: []})

    parents = sorted(parents, key=get_order)
    return render_template('manager/system_menu_page.html', parents=parents, menus=result)


@manager.route('/add_menu', methods=['GET', 'POST'])
@login_required
def add_menu():
    """
    添加菜单
    :return:
    """
    if request.method == 'POST':
        menu_name = request.form['menu_name']
        menu_url = request.form['menu_url']
        active = True if request.form.get('activate', 'off') == 'on' else False
        menu_icon = request.form['menu_icon']
        menu_desc = request.form['menu_desc']
        menu_order = request.form['menu_order']
        parent_id = request.form['parent_id']
        is_parent = False if parent_id else True
        new_menu = Menu()
        new_menu.menu_name = menu_name
        new_menu.menu_url = menu_url
        new_menu.active = active
        new_menu.menu_icon = menu_icon
        new_menu.menu_desc = menu_desc
        new_menu.menu_order = menu_order
        if parent_id:
            new_menu.parent_id = parent_id
        new_menu.is_parent = is_parent
        db.session.add(new_menu)
        db.session.commit()
        flash('菜单添加成功', 'success')
        return redirect(url_for('manager.show_menus'))
    else:
        menu_icons = SystemParameter.query.filter(SystemParameter.key == 'menu_icons').first().value.split(',')
        parent_menus = Menu.query.filter(Menu.is_parent).all()
        return render_template('manager/add_menu.html', menu=None, menu_icons=menu_icons, parent_menus=parent_menus)


@manager.route('/edit_menu/<int:menu_id>', methods=['GET', 'POST'])
@login_required
def edit_menu(menu_id):
    """
    修改菜单
    :param menu_id:
    :return:
    """
    menu = Menu.query.filter(Menu.id == menu_id).first()
    if request.method == 'POST':
        menu_name = request.form['menu_name']
        menu_url = request.form['menu_url']
        active = True if request.form.get('activate', 'off') == 'on' else False
        menu_icon = request.form['menu_icon']
        menu_desc = request.form['menu_desc']
        menu_order = request.form['menu_order']
        parent_id = request.form['parent_id']
        is_parent = False if parent_id else True
        if menu:
            menu.menu_name = menu_name
            menu.menu_url = menu_url
            menu.active = active
            menu.menu_icon = menu_icon
            menu.menu_desc = menu_desc
            menu.menu_order = menu_order
            if parent_id:
                menu.parent_id = parent_id
            menu.is_parent = is_parent
            db.session.add(menu)
            db.session.commit()
            flash('菜单修改成功', 'success')
        else:

            new_menu = Menu()
            new_menu.menu_name = menu_name
            new_menu.menu_url = menu_url
            new_menu.active = active
            new_menu.menu_icon = menu_icon
            new_menu.menu_desc = menu_desc
            new_menu.menu_order = menu_order
            if parent_id:
                new_menu.parent_id = parent_id
            new_menu.is_parent = is_parent
            db.session.add(new_menu)
            db.session.commit()
            flash('菜单添加成功', 'success')
        role = current_user.role
        if role and role.menu:
            menu_ids = [menu_id for menu_id in role.menu.split(',') if id]
            menus = [menu for menu in Menu.query.filter(
                db.and_(Menu.active == True,
                        Menu.id.in_(menu_ids))).order_by(Menu.menu_order).all()]
        else:
            menus = []
        session['menu'] = create_menu(menus)
        return redirect(url_for('manager.show_menus'))
    else:
        menu_icons = SystemParameter.query.filter(SystemParameter.key == 'menu_icons').first().value.split(',')
        parent_menus = Menu.query.filter(Menu.is_parent).all()
        return render_template('manager/add_menu.html', menu=menu, menu_icons=menu_icons, parent_menus=parent_menus)


def get_order(menu):
    if menu:
        return menu.menu_order
    else:
        return 0


@manager.route('/_menu_activate')
@login_required
def set_menu_activate():
    menu_id = request.args.get('id', 0, type=int)
    activate = request.args.get('activate')
    if activate == 'Enable':
        db.session.execute('UPDATE opts_menu SET active=1 WHERE id =%s or parent_id=%s' % (menu_id, menu_id))
    elif activate == 'Disable':
        db.session.execute('UPDATE opts_menu SET active=0 WHERE id =%s or parent_id=%s' % (menu_id, menu_id))
    db.session.commit()

    return '{"result": true}'


@manager.route('/role_manage')
@login_required
def role_manage():
    roles = Role.query.all()
    return render_template('manager/role_manage.html', roles=roles)


@manager.route('/add_role', methods=['GET', 'POST'])
@login_required
def add_role():
    if request.method == 'POST':
        role_name = request.form['rolename']
        index_page = request.form['indexpage']
        role = Role()
        role.name = role_name
        role.index_page = index_page
        old_role = Role.query.filter(Role.name == role_name).first()
        if old_role:
            flash('角色已经存在!', 'warning')
        else:
            db.session.add(role)
            db.session.commit()
            flash('角色添加成功!', 'success')
            return redirect(url_for('manager.role_manage'))
    return render_template('manager/role_add.html')


@manager.route('/edit_role/<int:role_id>', methods=['GET', 'POST'])
@login_required
def edit_role(role_id):
    role = Role.query.filter(Role.id == role_id).first()
    if request.method == 'POST':
        all_id = [str(menu_id) for menu_id in request.form.getlist('role_menu') if menu_id]

        if all_id:
            query_sql = "SELECT DISTINCT  parent_id FROM opts_menu WHERE id IN(%s)" % ','.join(all_id)

            for row in db.engine.execute(query_sql):
                if row[0] != 'None' and row[0] != None:
                    all_id.append(str(row[0]))

            role.menu = ','.join(list(set(all_id)))
        else:
            role.menu = ''

        role.name = request.form['name']
        role.index_page = request.form['index_page']

        db.session.add(role)
        db.session.commit()

        user_ids = request.form.getlist('role_member')
        member = User.query.filter_by(role_id=role.id).all()
        for user in member:
            if user.id in user_ids:
                user_ids.remove(user.id)
            else:
                user.role = None
                db.session.add(user)

        users = User.query.filter(User.id.in_(user_ids))
        for user in users:
            user.role = role
            db.session.add(user)
        db.session.commit()

        flash('修改成功', 'success')
        session['index_page'] = request.form['index_page']
        role = current_user.role
        if role and role.menu:
            menu_ids = [menu_id for menu_id in role.menu.split(',') if id]
            menus = [menu for menu in Menu.query.filter(
                db.and_(Menu.active == True,
                        Menu.id.in_(menu_ids))).order_by(Menu.menu_order).all()]
        else:
            menus = []
        session['menu'] = create_menu(menus)
        return redirect(url_for('manager.role_manage'))
    role_menu = [int(id) for id in role.menu.split(',') if id] if role.menu else []
    menus = Menu.query.all()
    users = User.query.all()
    return render_template('manager/role_edit.html', role=role, role_menu=role_menu, menus=menus, users=users)


@manager.route('/add_user', methods=['POST', 'GET'])
@login_required
def add_user():
    if request.method == 'POST':
        cn = request.form.get('cn')
        mail = request.form.get('mail')
        uid = request.form.get('uid')
        try:
            # 定义ldap服务器
            s = Server(Config.LDAP_HOST,
                       get_info=ALL)
            # 定义连接
            c = Connection(s, user=Config.LDAP_ADMIN_USER, password=Config.LDAP_PASSWD, auto_bind=True)
            # 添加用户
            c.add('cn=%s,%s' % (cn, Config.LDAP_SEARCH_BASE),
                  attributes={'objectClass': ['inetOrgPerson', 'top'], 'mail': mail, 'userPassword': '123456', 'sn': cn,
                              'uid': uid})
            c.unbind()
            flash('添加成功!', 'success')
        except Exception as e:
            flash('添加失败:%s' % str(e), 'warning')
        return redirect(url_for('manager.add_user'))
    return render_template('manager/user_add.html')


@manager.route('/system_para')
@login_required
def system_para():
    paras = SystemParameter.query.all()
    return render_template('manager/system_para.html', paras=paras)


@manager.route('/edit_para/<int:para_id>', methods=['POST', 'GET'])
@login_required
def edit_para(para_id):
    sys_para = SystemParameter.query.filter(SystemParameter.id == para_id).first()
    if request.method == "POST":
        key = request.form.get('sysname')
        value = request.form.get('sysvalue')
        desc = request.form.get('sysdesc')
        if key != sys_para.key:
            old_sys = SystemParameter.query.filter(SystemParameter.key == key).first()
            if old_sys:
                flash('此参数已经存在!!', 'warning')
                return redirect(url_for('manager.edit_para', para_id=para_id))
        sys_para.key = key
        sys_para.value = value
        sys_para.note = desc
        db.session.add(sys_para)
        db.session.commit()
        flash('参数修改成功!!', 'success')
        return redirect(url_for('manager.system_para'))
    return render_template('manager/sys_add.html', para=sys_para)


@manager.route('/add_para', methods=['POST', 'GET'])
@login_required
def add_para():
    if request.method == 'POST':
        sys_para = SystemParameter()
        key = request.form.get('sysname')
        value = request.form.get('sysvalue')
        desc = request.form.get('sysdesc')
        old_sys = SystemParameter.query.filter(SystemParameter.key == key).first()
        if old_sys:
            flash('此参数已经存在!!', 'warning')
        else:
            sys_para.key = key
            sys_para.value = value
            sys_para.note = desc
            db.session.add(sys_para)
            db.session.commit()
            flash('参数添加成功!!', 'success')
            return redirect(url_for('manager.system_para'))
    return render_template('manager/sys_add.html', para=None)


@manager.route('/show_organize')
@login_required
def show_organize():
    """
    展示组织架构
    :return:
    """
    organizations = Organization.query.all()
    parents = []
    result = {}
    for organization in organizations:
        if organization.parent and organization.parent in result.keys():
            result[organization.parent].append(organization)
        elif organization.parent:
            result.update({organization.parent: [organization]})
            if not organization.parent in parents:
                parents.append(organization.parent)
        else:
            if not organization in parents:
                parents.append(organization)
            result.update({organization.parent: []})
    return render_template('manager/show_organize.html', parents=parents, groups=result)


@manager.route('/add_organize', methods=['POST', 'GET'])
@login_required
def add_organize():
    """
    添加组织架构
    :return:
    """
    if request.method == 'POST':
        name = request.form.get('organize_name')
        parent_id = request.form.get('parent_id')
        is_parent = True if parent_id else False
        organize = Organization()
        organize.name = name
        organize.is_parent = is_parent
        if parent_id:
            organize.parent_id = parent_id
        old_org = Organization.query.filter(Organization.name == name).first()
        print(old_org)
        if old_org:
            flash('此组织已经存在!', 'warning')
        else:
            db.session.add(organize)
            db.session.commit()
            flash('组织添加成功!', 'success')
            return redirect(url_for('manager.show_organize'))
    parent_organizations = Organization.query.filter(Organization.parent == None).all()
    return render_template('manager/organize_add.html', organize=None, parent_organizations=parent_organizations)


@manager.route('/edit_organize/<int:org_id>', methods=['POST', 'GET'])
@login_required
def edit_organize(org_id):
    org = Organization.query.filter(Organization.id == org_id).first()
    if request.method == 'POST':
        name = request.form.get('organize_name')
        parent_id = request.form.get('parent_id')
        if name != org.name:
            old_org = Organization.query.filter(Organization.name == name).first()
            if old_org:
                flash('此组织已存在!', 'warning')
                return redirect(url_for('manager.edit_organize', org_id=org_id))
        org.name = name
        is_parent = True if parent_id else False
        org.is_parent = is_parent
        if parent_id:
            org.parent_id = parent_id
        else:
            org.parent_id = None
        db.session.add(org)
        db.session.commit()
        flash('组织信息修改成功!', 'success')
        return redirect(url_for('manager.show_organize'))
    parent_organizations = Organization.query.filter(Organization.parent == None).all()
    return render_template('manager/organize_add.html', organize=org, parent_organizations=parent_organizations)


@manager.route('/edit_user/<int:user_id>', methods=['POST', 'GET'])
@login_required
def edit_user(user_id):
    user = User.query.filter(User.id == user_id).first()
    organizes = Organization.query.all()
    roles = Role.query.all()
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        organize_id = request.form.get('organize_id')
        role_id = request.form.get('role_id')
        user.display_name = nickname
        user.organize_id = organize_id if organize_id else None
        user.role_id = role_id
        db.session.add(user)
        db.session.commit()
        flash('信息修改成功!', 'success')
        return redirect(url_for('manager.accounts_manage'))
    return render_template('auth/profile.html', user=user, organizes=organizes, roles=roles)
