#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by huangtao@oraro
from omp import db


class ManHour(db.Model):
    """
    工时统计
    """
    __tablename__ = 'omp_hours'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('omp_user.id'))
    user = db.relationship('User', backref=db.backref('omp_hours_user', order_by=id))
    app_id = db.Column(db.Integer, db.ForeignKey('omp_apps.id'))
    app = db.relationship('Apps', backref=db.backref('omp_hours_apps', order_by=id))
    hour = db.Column(db.Float)
    day = db.Column(db.Date)
