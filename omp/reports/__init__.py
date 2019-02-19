#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by huangtao@oraro
from flask import Blueprint

reports = Blueprint('reports', __name__)
from .views import *
