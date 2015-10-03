# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect, render_template
from neighbour.models.user import User
from flask_login import login_user, current_user, logout_user, user_logged_in
from neighbour.utils.request_params import get_request_params
account = Blueprint('account', __name__)
from neighbour.test.redirect_test import red

@account.route('/login', methods=["GET", "POST"])
def login():
    return red()
    # return redirect('http://www.baidu.com')
    print u'重定向'
    request_params = get_request_params(request)
    name = request_params.get('name')
    password = request_params.get('password')

    user = User.query.filter_by(login_name=name).first()
    if user:
        if user.check_password(password):
            login_user(user, remember=False)
            return redirect()
        else:
            return u'名称或密码不正确'
    if current_user:
        pass
        # print 'Logined no %s' % current_user.login_name

        # return 'Logined now %s' % current_user.login_name

    return 'Not Login'



@account.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return 'Logout Now'