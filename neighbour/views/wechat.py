# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

wechat = Blueprint('wechat', __name__)

@wechat.route('/index')
def index():
    return render_template('/wechat/index.shtml')

@wechat.route('/verify/submitForm.shtml')
def user_verify():
    return render_template('/wechat/submitForm.shtml')

@wechat.route('/myHouse.shtml')
def myhouse():
    return render_template('/wechat/myHouse.shtml')

@wechat.route('/service/meter.shtml')
def meter():
    return render_template('/wechat/meter.shtml')