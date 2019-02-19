#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by huangtao@oraro
from flask import flash, session, request, url_for, redirect, render_template
from flask_login import login_required, current_user
from . import apps
from .models import Apps
from omp import db


@apps.route('/all_apps')
@login_required
def all_apps():
    all_apps = Apps.query.all()
    return render_template('apps/all_apps.html', all_apps=all_apps)


@apps.route('/add_apps', methods=["GET", "POST"])
@login_required
def add_apps():
    if request.method == "POST":
        app_name = request.form.get('app_name')
        old_app = Apps.query.filter(Apps.name == app_name).first()
        if old_app:
            flash("此App已经存在!!", "warning")
            return redirect(url_for("apps.all_apps"))
        desc = request.form.get('desc')
        app = Apps()
        app.name = app_name
        app.desc = desc
        db.session.add(app)
        db.session.commit()
        flash("App添加成功!!", "success")
        return redirect(url_for("apps.all_apps"))

    return render_template('apps/app_add.html', app=None)