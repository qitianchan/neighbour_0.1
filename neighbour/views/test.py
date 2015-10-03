# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

test = Blueprint('test', __name__)

@test.route('/index')
def index():
    return render_template('index.html', title=u'你麻痹')