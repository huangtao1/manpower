#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by huangtao@oraro

# 注册blueprint
from flask import Blueprint


hours = Blueprint('hours', __name__)
from . import views