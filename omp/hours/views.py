#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by huangtao@oraro
from omp import db
from flask import session, render_template, url_for, current_app, request, flash, redirect
from flask_login import login_required, current_user
from . import hours
from omp.apps.models import Apps
from .models import ManHour


@hours.route('/add_hours', methods=['GET', 'POST'])
@login_required
def add_hours():
    """
    录入工时
    :return:
    """
    apps = Apps.query.all()
    if request.method == "POST":
        # 记录的时间
        day = request.form.get('day')
        # 查询每一条记录
        for key in request.form.keys():
            if key.startswith('app_id'):
                index = key.split('_')[-1]
                # 所属项目
                app_id = request.form.get('app_id_' + index)
                # 消耗时间
                hour = request.form.get('spend_hour_' + index)
                # 查询是否已经有此项目记录,如果有就更新数据
                man_hour = ManHour.query.filter(db.and_(ManHour.app_id == app_id,ManHour.user_id == current_user.id,ManHour.day == day)).first()
                if not man_hour:
                    man_hour = ManHour()
                man_hour.app_id = app_id
                man_hour.user_id = current_user.id
                man_hour.day = day
                man_hour.hour = hour
                db.session.add(man_hour)
                db.session.commit()
        flash('工时录入成功', 'success')
        return redirect(url_for('hours.my_hours'))
    return render_template('hours/add_hours.html', apps=apps)


@hours.route('/my_hours')
@login_required
def my_hours():
    """
    查看自己的工时
    :return:
    """
    my_hours = ManHour.query.filter(ManHour.user_id == current_user.id).order_by(ManHour.day.desc()).all()
    return render_template('hours/my_hours.html', hours=my_hours)
