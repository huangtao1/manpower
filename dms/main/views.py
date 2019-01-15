#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by mark.huang on 2018/6/27.
from . import main
from flask_login import login_required, current_user
from flask import redirect, url_for, render_template


@main.route('/')
@login_required
def mains():
    return redirect(url_for(current_user.role.index_page))


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('main/404.html'), 404


@main.app_errorhandler(502)
def page_not_found(e):
    return render_template('main/error.html', error='502'), 500


@main.app_errorhandler(500)
def page_not_found(e):
    return render_template('main/error.html', error='500'), 500
