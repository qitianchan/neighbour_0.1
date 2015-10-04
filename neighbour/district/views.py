# -*- coding: utf-8 -*-

from flask import Blueprint, request, redirect, flash, url_for
from flask import render_template
from jinja2 import TemplateNotFound
from flask import abort
from flask_login import (login_user, current_user, login_required, logout_user)
from neighbour.wechatcache.wechatcache import WechatBasicCache


distric = Blueprint('distric', __name__, template_folder='templates')


@distric.route('/', methods=['GET', 'POST'])
def hello():
    return 'Hello World'

@distric.route('/user_auth')
def user_auth():
    w = WechatBasicCache(appid='wxfffccad204419582', appsecret='2091a0d282ded114af1ce4839c92d87a')

    if request.args.get('code', None) == None:
        return w.authorize(scope='snsapi_userinfo')

    userinfo = w.authorize(scope='snsapi_userinfo')

    print userinfo.keys()

    return '23'







