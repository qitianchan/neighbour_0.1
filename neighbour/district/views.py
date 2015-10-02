# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from flask import Blueprint, request, redirect, flash, url_for
from flask import render_template
from jinja2 import TemplateNotFound
from flask import abort
from flask_login import (login_user, current_user, login_required, logout_user)


distric = Blueprint('distric', __name__, template_folder='templates')


@distric.route('/', methods=['GET', 'POST'])
def hello():
    return 'Hello World'

