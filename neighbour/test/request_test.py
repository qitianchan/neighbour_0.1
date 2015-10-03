# -*- coding: utf-8 -*-
import urllib
import urllib2
import requests


url = 'http://localhost:8001/account/login'


def post_request(values):
    assert isinstance(values, dict)
    data = urllib.urlencode(values)
    print data
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()
    print the_page

def get_requst(data):
    assert isinstance(data, dict)
    r = requests.get(url, params=data)
    print r.text


if __name__ == '__main__':
    values = {
        'name': 'qitian',
        'password': 'aaaaaa'
    }
    # post_request(values)
    get_requst(data=values)