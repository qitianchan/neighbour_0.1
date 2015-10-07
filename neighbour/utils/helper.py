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


def ret_dict(res_code='0000'):
    ret = dict()
    if res_code == '0000':
        ret['resCode'] = '0000'
        ret['resMsg'] = u'操作成功'
    elif res_code == '1000':
        ret['resCode'] = '1000'
        ret['resMsg'] = u'未登录'
    elif res_code == '2000':
        ret['resCode'] = '2000'
        ret['resMsg'] = u'未认证'
    elif res_code == '3000':
        ret['resCode'] = '3000'
        ret['resMsg'] = u'参数错误'
    elif res_code == '5000':
        ret['resCode'] = '5000'
        ret['resMsg'] = u'服务器错误'
    else:
        ret['resCode'] = '5100'
        ret['resMsg'] = u'未知错误'
    return ret


def get_all_element_in_list(li):
    """
    返回li列表中又有元素的列表
    :param li: 列表  e.g. li=[343,[12,34],[344,[2],[478,202]]]
    :return: 列表 return_list = [343, 12, 34, 344, 2, 478, 202]
    """
    all_element_list = []
    return middle_func(li, all_element_list)


def middle_func(li, all_element_list):
    for element in li:
        if isinstance(element, list):
                middle_func(element, all_element_list)
        else:
            all_element_list.append(element)
    return all_element_list
