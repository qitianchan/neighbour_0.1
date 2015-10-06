# -*- coding: utf-8 -*-
from neighbour.models.residential_areas import ResidentialAreas
from flask import Blueprint, jsonify, request, session, redirect, url_for
from neighbour.models.user import User
from neighbour.models.house_info import UserHouseTable
from neighbour.models.house_fee import HouseFee
from sqlalchemy import and_, select
wechat_front = Blueprint('wechat_front', __name__)
from neighbour.extensions import db
from neighbour.configs.default import DefaultConfig
import time
from sqlalchemy.exc import IntegrityError


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
    except Exception, ex:
        final_return = {
            'retCode': '5000',
            'retMsg': ex.message
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
    except Exception, ex:
        ret = {
            'retCode':'5000',
            'retMsg': ex.message
        }
    return jsonify(ret)


@wechat_front.route('/upload_bill_data')
def upload_bill_data():
    """
    上传燃气表、水表接口
    :param house_code:house_id
    :param type:电表或是燃气表
    :param num:度数
    :return:
    """
    ret = {
        'retCode': '0000',
        'retMsg': ''
    }
    args = request.args
    type = args.get('type')
    house_info_id = args.get('house_code')
    num = args.get('num')
    fee = HouseFee.get_last_mon_fee(house_info_id=house_info_id)
    if fee == None:
        fee = HouseFee()
        fee.house_info_id = house_info_id
        time_struct = time.localtime()
        year = time_struct.tm_year
        mon = time_struct.tm_mon - 1
        if(mon < 1):
            year -= 1
        fee.year = year
        fee.month = mon

    if type == str(DefaultConfig.WATER):
        fee.water_num = num
    elif type == str(DefaultConfig.GAS):
        fee.gas_num = num

    try:
        fee.save()
    except IntegrityError:
        ret = {
            'retCode': '3000',
            'retMsg': 'house_code不存在！请确认house_code正确'
        }
    except Exception , ex:
        ret = {
            'retCode': '5000',
            'retMsg': ex.message
        }

    return jsonify(ret)


@wechat_front.route('/get_month_bill_status')
def get_month_bill_status():
    """
    获取当前年的有无费用
    :return:
    """
    args = request.args
    house_info_id = args.get('house_code')
    current_time = time.localtime()
    current_year = current_time.tm_year
    current_mon = current_time.tm_mon
    monthList = [str(current_year) + "%02d" % mon  + '0' for mon in range(1, 13)]

    fees = HouseFee.get_year_fees(house_info_id=house_info_id)
    for fee in fees:
        index = fee.month - 1
        monthList[index] = str(current_year) + '%02d' % fee.month + '1'

    ret = {
        'retCode': '0000',
        'retMst': '',
        'monthList': monthList,
        'currentMon': str(current_year) + '%02d' % current_mon
    }

    return jsonify(ret)


@wechat_front.route('/get_bill')
def get_bill():
    args = request.args
    house_info_id = args.get('house_code')
    year_mon = args.get('year_mon')
    ret = {
        'retCode': '0000',
        'retMsg': '',
        'billList':[],
        'lastMonth': '',
        'nextMonth': ''
    }
    year = None
    mon = None
    last_year = None
    last_mon = None
    next_year = None
    next_mon = None
    def get_last_mon(year, mon):
        last_mon = None
        last_year = None
        if mon == 1:
            last_year = year - 1
            last_mon = 12
        elif mon == 12:
            last_year = year
            last_mon -= 1
        else:
            last_year = year
            last_mon = mon - 1
        return (last_year, last_mon)

    def get_next_mon(year, mon):
        next_year = None
        next_mon = None
        if mon == 1:
            next_year = year
            next_mon += 1
        elif mon == 12:
            next_year = year + 1
            next_mon = 1
        else:
            next_year = year
            next_mon = mon + 1
        return (next_year, next_mon)

    try:
        year = int(year_mon[:4])
        mon = int(year_mon[4:])
        last_year, last_mon = get_last_mon(year, mon)
        next_year, next_mon = get_last_mon(year, mon)

    except ValueError as ex:
        ret = {
            'retCode': '3000',
            'retMsg': '年月格式错误，请按照201509的格式传递',
            'billList':[],
            'lastMonth': '',
            'nextMonth': ''
        }

    mon_list = [
        {
            'year': year,
            'mon': mon
        },
        {
            'year': last_year,
            'mon': last_mon
        },
        {
            'year': next_year,
            'mon': next_mon
        },
    ]
    fees = HouseFee.get_house_fees(house_info_id=house_info_id,monList=mon_list)
    fees_dict = {}
    if fees:
        for fee in fees:
            fees_dict[fee.month] = fee
        target_fee = None
        total_fee = 0
        try:
            target_fee = fees_dict[mon]
            total_fee = target_fee.water_fee + target_fee.gas_fee + target_fee.electricity_fee
            ret['total'] = total_fee

            last_mon_fee = None
            if fees_dict.has_key(last_mon):
                ret['lastMonth'] = str(last_year) + "%02d" % last_mon
                last_mon_fee = fees_dict[last_mon]
                ret['billList'] = [
                    {
                        'FeeID': target_fee.id,
                        'fee': target_fee.water_fee,
                        'name': '水费',
                        'status': target_fee.water_fee_status,
                        'detailList': {
                            'thisMon': target_fee.water_num,
                            'lastMon': last_mon_fee.water_num
                        }
                    },
                    {
                        'FeeID': target_fee.id,
                        'fee': target_fee.gas_fee,
                        'name': '燃气费',
                        'status': target_fee.gas_fee_status,
                        'detailList': {
                            'thisMon': target_fee.gas_num,
                            'lastMon': last_mon_fee.gas_num
                        }
                    },
                    {
                        'FeeID': target_fee.id,
                        'fee': target_fee.electricity_fee,
                        'name': '电费',
                        'status': target_fee.electricity_fee_status,
                        'detailList': {
                            'thisMon': target_fee.electricity_num,
                            'lastMon': last_mon_fee.electricity_num
                        }
                    },

                ]
            else:
                ret['billList'] = [
                    {
                        'FeeID': target_fee.id,
                        'fee': target_fee.water_fee,
                        'name': '水费',
                        'status': target_fee.water_fee_status,
                        'detailList': {
                            'thisMon': target_fee.water_num,
                            'lastMon': 0
                        }
                    },
                    {
                        'FeeID': target_fee.id,
                        'fee': target_fee.gas_fee,
                        'name': '燃气费',
                        'status': target_fee.gas_fee_status,
                        'detailList': {
                            'thisMon': target_fee.gas_num,
                            'lastMon': 0
                        }
                    },
                    {
                        'FeeID': target_fee.id,
                        'fee': target_fee.electricity_fee,
                        'name': '电费',
                        'status': target_fee.electricity_fee_status,
                        'detailList': {
                            'thisMon': target_fee.electricity_num,
                            'lastMon': 0
                        }
                    },

                ]

        except IndexError as ex:
            if fees_dict.has_key(last_mon):
                ret['lastMonth'] = str(last_year) + "%02d" % last_mon


        if fees_dict.has_key(next_mon):
            ret['nextMonth'] = str(next_year) + "%02d" % next_mon

    else:
        pass

    return jsonify(ret)



@wechat_front.route('/test')
def test():
    return str(session['current_user_id'])


if __name__ == "__main__":
    monthList = [str(2015) + "%02d" % mon for mon in range(1, 13)]
    print monthList
    print "%02d" % 11
    year_mon = '03'
    year = int(year_mon[:4])
    print year
    try:
        mon = int(year_mon[4:])
    except ValueError as ex:
        print ex.message

    print 3 + None

