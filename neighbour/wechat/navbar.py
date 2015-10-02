# -*- coding: utf-8 -*-
from flask import Blueprint

wechat_navbar = Blueprint('wechat_navbar', __name__)


@wechat_navbar.route('/set_menu', methods=['GET'])
def set_menu():
    return 'hello world'
