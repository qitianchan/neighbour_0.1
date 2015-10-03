# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from flask import Blueprint, request, redirect, flash, url_for
from flask import render_template
from jinja2 import TemplateNotFound
from flask import abort
from flask_login import (login_user, current_user, login_required, logout_user)
from wechat_sdk import WechatBasic


valiation_app = Blueprint('valiation', __name__, template_folder='templates')


@valiation_app.route('/jfjl_valiation', methods=['GET', 'POST'])
def jfjl_valiation():
    args = request.args
    token = 'jiefangjieli'
    echostr = args['echostr']
    signature = args['signature']
    timestamp = args['timestamp']
    nonce = args['nonce']
    wechat = WechatBasic(token=token)
    # 对签名进行校验
    if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
        return echostr
    else:
        return "This is jfjl valiation!"




