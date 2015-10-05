#****coding=utf-8********
__author__ = 'Chan'

from wechat_api import wechat_front
from flask import render_template, request

@wechat_front.route('/new_test')
def new_test():
    return 'bad bad'
