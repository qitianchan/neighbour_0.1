# -*- coding: utf-8 -*-

def get_request_params(request):
    if request.method == 'POST':
        parmas = request.form
    elif request.method == 'GET':
        parmas = request.args
    return parmas
