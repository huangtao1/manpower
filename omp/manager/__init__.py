#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by mark.huang on 2018/7/2.
from flask import Blueprint

manager = Blueprint('manager', __name__)
from . import views
