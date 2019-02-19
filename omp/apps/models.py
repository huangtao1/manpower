#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by huangtao@oraro
from omp import db


class Apps(db.Model):
    """
    应用表
    """
    __tablename__ = 'omp_apps'

    id = db.Column(db.Integer, primary_key=True)
    # app名称
    name = db.Column(db.String(200), unique=True)
    desc = db.Column(db.String(200))