#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by mark.huang on 2018/6/27.
from flask import Blueprint

main = Blueprint('', __name__)
from . import views
