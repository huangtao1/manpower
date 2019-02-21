#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by huangtao@oraro
from . import reports
from flask import url_for, redirect, request, render_template, send_from_directory
from flask_login import login_required
from omp.auth.models import User
from sqlalchemy import func
from omp import db
from omp.hours.models import ManHour
from omp.apps.models import Apps
import json
from datetime import datetime
from config import Config
import os
import xlwt


@reports.route('/hour_reports')
@login_required
def hour_reports():
    """
    工时收集,默认展示当天
    :return:
    """
    users = User.query.all()
    start_day = datetime.now().strftime('%Y-%m-%d')
    all_app_hours, user_app_hours = get_project_data(start_day=start_day, end_day=start_day)
    return render_template('reports/hour_reports.html', users=users, all_app_hours=all_app_hours,
                           user_app_hours=user_app_hours)


@reports.route('/get_hour_data_info', methods=['POST'])
@login_required
def get_hour_data_info():
    start_day = request.form.get('start_day') if request.form.get('start_day') else datetime.strftime(datetime.now(),
                                                                                                      '%Y-%m-%d')
    end_day = request.form.get('end_day') if request.form.get('start_day') else datetime.strftime(datetime.now(),
                                                                                                  '%Y-%m-%d')
    user_id = int(request.form.get('user_id'))
    all_app_hours, user_app_hours = get_project_data(start_day=start_day, end_day=end_day, user_id=user_id)
    return json.dumps({'all_app_hours': all_app_hours, 'user_app_hours': user_app_hours})


@reports.route('/export_hour_data')
@login_required
def export_hour_data():
    """导出数据"""
    # 获取今天日期
    today = datetime.strftime(datetime.now(), '%Y-%m-%d')
    # 获取月份
    month = datetime.strftime(datetime.now(), '%Y-%m')
    # 起始时间
    start_day = month + '-01'
    # 查哪些项目有数据,同时统计总数
    all_apps = Apps.query.all()
    all_app_hours = []
    has_hour_apps = []
    user_hour_infos = []
    user_total_info = {}
    all_users = User.query.all()
    # 项目数据
    for app in all_apps:
        # 查询每个项目的总工时
        score = db.session.query(func.sum(ManHour.hour)).filter(
            db.and_(ManHour.app_id == app.id, ManHour.day.between(start_day, today))).scalar()
        # 如果有数据就收集
        if score:
            has_hour_apps.append(app)
            hour_info = {app.name: float('%.1f' % score)}
            all_app_hours.append(hour_info)
    # 所有项目总工时
    apps_total = db.session.query(func.sum(ManHour.hour)).filter(ManHour.day.between(start_day, today)).scalar()
    total_info = {'total': float('%.1f' % apps_total)}
    # 个人数据
    for user in all_users:
        if user.username in ['tianyong']:
            continue
        user_hour_info = {'username': user.display_name}
        user_app_infos = []
        for has_hour_app in has_hour_apps:
            user_sum = db.session.query(func.sum(ManHour.hour)).filter(
                db.and_(ManHour.app_id == has_hour_app.id, ManHour.day.between(start_day, today),
                        ManHour.user_id == user.id)).scalar()
            sum_hour = float('%.1f' % user_sum) if user_sum else 0
            user_app_infos.append({has_hour_app.name: sum_hour})
        user_all_sum = db.session.query(func.sum(ManHour.hour)).filter(
            db.and_(ManHour.day.between(start_day, today),
                    ManHour.user_id == user.id)).scalar()
        sum_hour = float('%.1f' % user_all_sum) if user_all_sum else 0
        user_total_info[user.display_name] = sum_hour
        user_hour_info['info'] = user_app_infos
        user_hour_infos.append(user_hour_info)
    # 生成Excel
    # 字体风格
    font = xlwt.Font()
    font.name = '等线'
    # 字体大小*20
    font.height = 220
    # 边框风格
    borders = xlwt.Borders()
    borders.right = xlwt.Borders.THIN
    borders.left = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN
    # 标题风格
    title_style = xlwt.XFStyle()  # 创建一个样式对象，初始化样式
    al = xlwt.Alignment()
    al.horz = 0x02  # 设置水平居中
    al.vert = 0x01  # 设置垂直居中
    title_style.alignment = al
    title_style.font = font
    title_style.borders = borders
    # 正文风格
    body_style = xlwt.XFStyle()
    body_al = xlwt.Alignment()
    body_al.horz = 0x01  # 设置水平靠左
    al.vert = 0x01  # 设置垂直居中
    body_style.alignment = body_al
    body_style.font = font
    body_style.borders = borders
    # 创建excel
    excel_name = '研发中心%s月工时报表%s.xls' % (month, datetime.now().strftime("%Y%m%d%H%M%S"))
    excel_path = os.path.join(Config.EXCEL_DIR, excel_name)
    excel = xlwt.Workbook(encoding='utf-8')
    sheet = excel.add_sheet('%s月工时报表' % month)
    for i in range(len(has_hour_apps) + 1):
        if i == 0:
            sheet.col(i).width = 256 * 10
        sheet.col(i).width = 256 * 20
    sheet.write_merge(0, 0, 0, len(has_hour_apps) + 1, '研发中心%s月工时报表(单位h)' % month, title_style)
    sheet.write(1, 0, '姓名', body_style)
    for i in range(len(has_hour_apps)):
        sheet.write(1, i + 1, has_hour_apps[i].name, body_style)
    sheet.write(1, len(has_hour_apps) + 1, '总计', body_style)
    user_no = 2
    for user_hour_info in user_hour_infos:
        # 姓名
        sheet.write(user_no, 0, user_hour_info['username'], body_style)
        # 项目时间
        for i in range(len(has_hour_apps)):
            for hour_info in user_hour_info['info']:
                if has_hour_apps[i].name in hour_info:
                    sheet.write(user_no, i + 1, hour_info[has_hour_apps[i].name], body_style)
        sheet.write(user_no, len(has_hour_apps) + 1, user_total_info[user_hour_info['username']], body_style)
        user_no += 1
    # 总时间
    sheet.write(user_no, 0, '总计', body_style)
    for i in range(len(has_hour_apps)):
        for app_total in all_app_hours:
            if has_hour_apps[i].name in app_total:
                sheet.write(user_no, i + 1, app_total[has_hour_apps[i].name], body_style)
    sheet.write(user_no, len(has_hour_apps) + 1, total_info['total'], body_style)
    excel.save(excel_path)
    return send_from_directory(Config.EXCEL_DIR, excel_name, as_attachment=True,
                               attachment_filename=excel_name)


def get_project_data(start_day, end_day, user_id=1):
    """
    统计工时数据
    :param start_day:
    :param end_day:
    :param user_id:
    :return:
    """
    all_apps = Apps.query.all()
    all_app_hours = []
    user_app_hours = []
    for app in all_apps:
        # 查询每个项目的总工时
        score = db.session.query(func.sum(ManHour.hour)).filter(
            db.and_(ManHour.app_id == app.id, ManHour.day.between(start_day, end_day))).scalar()
        # 如果有数据就收集
        if score:
            hour_info = {'project': app.name, 'hours': float('%.1f' % score)}
            all_app_hours.append(hour_info)
        # 查询单个用户的项目总工时
        user_score = db.session.query(func.sum(ManHour.hour)).filter(
            db.and_(ManHour.app_id == app.id, ManHour.day.between(start_day, end_day),
                    ManHour.user_id == user_id)).scalar()
        if user_score:
            user_hour_info = {'project': app.name, 'hours': float('%.1f' % user_score)}
            user_app_hours.append(user_hour_info)
    return all_app_hours, user_app_hours
