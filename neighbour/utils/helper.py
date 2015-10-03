# -*- coding: utf-8 -*-
from random import Random
from hashlib import sha1

def create_salt():
    salt = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    len_chars = len(chars) - 1
    random = Random()
    for i in xrange(32):
        # 每次从chars中随机取一位
        salt += chars[random.randint(0, len_chars)]
    return salt


def create_sha1_password(password):
        salt = create_salt()
        alt = create_salt()
        sha1_obj = sha1()
        sha1_obj.update(password+salt)
        password = sha1_obj.hexdigest
        return (password, sha1)