# -*- coding: utf-8 -*-
from neighbour.models.residential_areas import ResidentialAreas
from flask import Blueprint, jsonify, request, session, redirect, url_for
from neighbour.models.user import User
from neighbour.models.house_info import UserHouseTable
from sqlalchemy import and_, select
wechat_front = Blueprint('wechat_front', __name__)
from neighbour.extensions import db

def get_current_user_openid():
    return '131243214'





@wechat_front.route('/get_areas', methods=['GET'])
def get_areas():
    residential_areas = ResidentialAreas.get_areas()
    result = {}
    final_return = None
    try:
        for r in residential_areas:
            if result.has_key(r.zone_id):
                result[r.zone_id]['areaList'].append({
                    'areaID': r.id,
                    'areaName': r.area_name
                })
            else:
                result[r.zone_id] = {
                    'zoneID': r.zone_id,
                    'zoneName': r.zone.area_name,
                    'areaList': [{
                        'areaID': r.id,
                        'areaName': r.area_name
                    }]
                }
        data = list()
        for key in result.keys():
            data.append(result[key])

        final_return = {
            'retCode': '0000',
            'retMsg': '',
            'zoneList': data
        }
    except Exception:
        final_return = {
            'retCode': '5000',
            'retMsg': Exception.message
        }

    return jsonify(final_return)


@wechat_front.route('/get_area_by_code', methods=['GET'])
def get_area_by_code():
    args = request.args
    code = args.get('code')
    return_data = {
        'retCode': '0000',
        'retMsg': ''
    }
    if code == None:
        return_data = {
            'retCode': '3000',
            'retMsg': 'code为空'
        }
    else:
        data = ResidentialAreas.get_area_info(area_id=code)
        if data:
            return_data['cellList'] = data['cellList']

    return jsonify(return_data)


@wechat_front.route('/get_user_house_info', methods=['GET'])
def get_user_house_info():
    # TODO: 通过opneid获取用户信息
    openid = get_current_user_openid()
    user = User.get_user_by_openid(openid)
    info_list = []
    info = {}
    ret = {}
    if user:
        for accocs in user.house_accocs:
            house = accocs.house
            if house:
                info['houseCode'] = house.id
                info['address'] = house.building.cell.cell_name + house.building.building_name + house.room_number   # 小区 + 楼栋 +　门牌号
                info['userType'] = accocs.user_type
                info_list.append(info)

                ret = {
                    'retCode': '0000',
                    'retMsg': 'success',
                    'userPhone': user.phone,
                    'houseInfoList': info_list
                }
            else:
                ret = {
                    'retCode': '3000',
                    'retMsg': '该用户没有对应房产信息'
                }
    else:
        ret = {
            'retCode': '3000',
            'retMsg': '没有对应用户'
        }

    return jsonify(ret)


@wechat_front.route('/update_house_info')
def update_house_info():
    """
    更新房产信息，TODO：也许需要在用户和房屋关联表中添加phone和name
    :return:
    """
    openid = get_current_user_openid()
    user = User.get_user_by_openid(openid)
    args = request.args
    house_id = args.get('code')
    user_house = UserHouseTable.get_user_house(user.id, house_id)
    ret = {
        'retCode': '0000',
        'retMsg': ''
    }
    if user_house:
        user_house.user_type = args.get('type')
    user.phone = args.get('phone')
    user.login_name = args.get('name')

    try:
        if user_house:
            user_house.save()
        user.save()
    except Exception:
        ret = {
            'retCode':'5000',
            'retMsg': Exception.message
        }
    return jsonify(ret)





@wechat_front.route('/test')
def test():
    return str(session['current_user_id'])


if __name__ == "__main__":
    pass