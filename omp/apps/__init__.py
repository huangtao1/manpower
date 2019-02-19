#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by huangtao@oraro
from flask import Blueprint

apps = Blueprint('apps', __name__)
from . import views
