# -*- coding: utf-8 -*-
from neighbour.models.residential_areas import ResidentialAreas
from flask import Blueprint, jsonify, request, session, redirect, url_for, send_file, render_template
from neighbour.models.user import User
from neighbour.models.house_info import UserHouseTable
from neighbour.models.house_fee import HouseFee
from neighbour.models.tenant import Tenant
from sqlalchemy import and_, select
wechat_front = Blueprint('wechat_front', __name__)
from neighbour.extensions import db
from neighbour.configs.default import DefaultConfig
import time
from sqlalchemy.exc import IntegrityError
from neighbour.models.house_info import HouseInfo
from neighbour.models.house_info import UserHouseTable
from neighbour.models.fix_order import FixOrder
from neighbour.models.fix_order_img import FixOrderImg
from neighbour.models.groupon import Groupon
from neighbour.models.groupon import GrouponOrderAreaOccocs
from neighbour.models.groupon_order import GrouponOrder
from neighbour.models.product import Product
from neighbour.models.product_image import ProductImage
from neighbour.models.customer_reviews import CustomerReviews
import time
from neighbour.configs.default import DefaultConfig as Config
from neighbour.extensions import db
from uuid import uuid1
import os
from neighbour.utils.helper import ret_dict, get_all_element_in_list


from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                              'static/upload/fix_order_img'))

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
    ret = {}
    if user:
        for accocs in user.house_accocs:
            house = accocs.house
            if house:
                info = {}
                info['houseCode'] = house.id
                info['address'] = house.building.cell.cell_name + house.building.building_name + house.room_number   # 小区 + 楼栋 +　门牌号
                info['userType'] = accocs.user_type
                info['userPhone'] = accocs.user_phone
                info_list.append(info)

                ret = {
                    'retCode': '0000',
                    'retMsg': 'success',
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



@wechat_front.route('/get_tenant')
def get_tenant():
    """
    获取房子住户
    :return:
    """
    house_info_id = request.args.get('house_code')
    tenants = Tenant.get_tenants(house_info_id=house_info_id)
    ret = {
        'retCode': '0000',
        'retMsg': '',
        'tenantList': [
            {
                'user_id': tenant.id,
                'name': tenant.name,
                'phone': tenant.phone,
                'type': tenant.tenant_type
            }for tenant in tenants
        ]
    }

    return jsonify(ret)

@wechat_front.route('/delete_tenant')
def delete_tenant():
    """
    删除关联用户
    :return:
    """
    args = request.args
    tenant_id = args.get('tenant_id')
    print Tenant.delete_tenants(tenant_id = tenant_id)
    ret = {
        'retCode': '0000',
        'retMsg': ''
    }
    return jsonify(ret)


@wechat_front.route('/test')
def test():
    return str(session['current_user_id'])


@wechat_front.route('/delete_house_info', methods=['GET', 'POST'])
def delete_house_info():
    if request.method == 'POST':
        house_id = request.form.get('house_code')
        if house_id is None:
            return jsonify({
                'retCode': '3000',
                'retMsg': '参数错误'
            })
        # TODO get_current_user_openid()  未实现
        user = User.get_user_by_openid(get_current_user_openid())
        if user:
            user_id = user.id
            user2house = UserHouseTable.get_user_house(user_id, house_id)
            if user2house:
                db.session.delete(user2house)
                db.session.commit()
                return jsonify({
                    'retCode': '0000',
                    'retMsg': '删除成功'
                })
            else:
                # 不错在用户的对应关系
                return jsonify({
                    'retCode': '3000',
                    'retMsg': '没有对应的关系'
                })
    return jsonify({
        'retCode': '5000',
        'retMsg': '未知错误'
    })


@wechat_front.route('/fix_order', methods=['GET', 'POST'])
def fix_order():
    # 获取参数
    if request.method != 'POST':
        return jsonify({
            'retCode': '3000',
            'retMsg': '没有对应的关系'
        })

    house_code = request.args.get('house_code')
    content = request.args.get('content')
    timestr = request.args.get('timestr')
    addr = request.args.get('addr')

    # 保存修理订单
    fix_order = FixOrder()
    fix_order.house_info_id = house_code
    fix_order.problem = content
    fix_order.time = timestr
    fix_order.create_time = int(time.time())
    fix_order.status = Config.FIX_ORDER_STATUS_IN_HAND

    db.session.add(fix_order)
    db.session.flush()

    # 保存图片
    for img_name in request.files.keys():
        img = request.files[img_name]
        if len(img_name.split('.')) >= 2:
            img_name = uuid1().hex + '.' + img_name.split('.')[-1]
        else:
            img_name = uuid1().hex

        img.save(UPLOAD_FOLDER + '\\' + img_name)

        # img.save(img.filename.encode('utf8'))
        fix_order_img = FixOrderImg()
        fix_order_img.img_name = img_name
        fix_order_img.fix_order_id = fix_order.id
        db.session.add(fix_order_img)


@wechat_front.route('/delete_fix_order', methods=['GET', 'POST'])
def delete_fix_order():
    #TODO:to fix
    fix_order_id = request.args.get('fix_order_id')
    if not fix_order_id:
        return jsonify(ret_dict('3000'))

    try:
        db.session.commit()
    except Exception, e:
        db.session.rollback()
        raise e
    return jsonify(ret_dict('0000'))







@wechat_front.route('/fix_order_list', methods=['GET', 'POST'])
def fix_order_list():
    open_id = get_current_user_openid()
    user = User.get_user_by_openid(open_id)
    if user:
        # 获取所有的修理订单
        fix_order_list = []
        for accocs in user.house_accocs:
            house = accocs.house
            if house:
                fix_order_list.append(house.fix_orders)

        fix_order_list = get_all_element_in_list(fix_order_list)
        # 格式化返回数据
        ret = ret_dict()
        data_list = []

        for order in fix_order_list:
            data = {
                'fixOrderID': order.id,
                'content': order.problem,
                'timeStr': order.time,
                'status': order.status
            }
            data_list.append(data)
        ret['fixOrderList'] = data_list
        return jsonify(ret)
    else:
        return jsonify(ret_dict('3000'))


@wechat_front.route('/get_fix_order_img/<img_name>')
def get_fix_order_img(img_name):
    # TODO: 使用Nginx作为静态文件的服务器
    return send_file(os.path.join(UPLOAD_FOLDER, img_name))


@wechat_front.route('/test_fix_img')
def test_fix_img():
    return render_template('wechat/fix_img.html')


@wechat_front.route('/get_fix_order_profile/<fix_order_id>')
def get_fix_order_profile(fix_order_id):
    # 获取基本信息
    fix_order = FixOrder.get_by_id(fix_order_id)
    if fix_order is None:
        return ret_dict('3000')
    house = fix_order.house_info
    data = {
        'houseCode': fix_order.house_info_id,
        'content': fix_order.problem,
        'timeStr': fix_order.time,
        'addr': house.building.cell.cell_name + house.building.building_name + house.room_number,
        'status': fix_order.status
    }

    # 获取图片列表，返回图片的url
    imgs = fix_order.imgs
    imgURLs = []
    for img in imgs:
        img_name = get_fix_order_img_url(img.img_name)
        imgURLs.append(img_name)
    data['imgURLs'] = imgURLs
    ret = ret_dict()
    ret['fixOrder'] = data
    return jsonify(ret)

@wechat_front.route('/get_groupon_detail')
def get_groupon_detail():
    """
    获取团购详情
    :return:
    """
    groupon_id = request.args.get('groupon_id')
    groupon = Groupon.get_groupon(groupon_id)
    product = groupon.product
    product_imgas = product.images
    ret = ret_dict()
    if not groupon:
        ret = ret_dict('3000')
        ret['retMsg'] = '找不到团购详情'
    else:
        info = {
            'status': groupon.groupon_status,
            'title': groupon.title,
            'price': groupon.groupon_price,
            'originPrice': product.orginal_price,
            'endTime': groupon.end_time,
            'shipWay': groupon.ship_way,
            'shipping_fee': groupon.shipping_fee,
            'count': groupon.sold_count,
            'product_content': product.content,
            'product_imgs': [{
                'img_url': img.img_url,
                'img_order': img.order
            }for img in product.images],
            'uuid': groupon.profile_img
        }
    ret = dict(ret, **info)
    return jsonify(ret)


@wechat_front.route('/get_groupon_customer_reviews')
def get_groupon_customer_reviews():
    groupon_id = request.args.get('groupon_id')
    if not groupon_id:
        ret = ret_dict('3000')
        return jsonify(ret)
    page_count = request.args.get('page_count', 20)
    page_num  = request.args.get('page', 1)
    index_start = (page_num - 1) * 20
    index_end = index_start + page_count
    statics_data = CustomerReviews.get_statics_data(groupon_id)
    groupon = Groupon.get_groupon(groupon_id)
    reviews = groupon.customer_reviews[index_start: index_end]
    ret = ret_dict('0000')
    data = {
        'vagScore': statics_data['avg_score'],
        'reviewsCount': statics_data['reviews_count'],
        'pageCount': page_count,
        'page': page_num,
        'sum': len(reviews),
        'reviewList': [{
            'userID': review.user.id,
            'nickname': review.user.wechat_nickname,
            'score': review.score,
            'content': review.content,
            'uuid': review.user.headimg_url
        }for review in reviews]
    }

    return jsonify(dict(ret, **data))



def get_fix_order_img_url(img_name):
    # TODO: 如果用Nginx作为静态文件服务器，这个函数需要改写
    return url_for('wechat_front.get_fix_order_img', img_name=img_name)




if __name__ == "__main__":
    monthList = [str(2015) + "%02d" % mon for mon in range(1, 13)]
    print monthList
    print "%02d" % 11
    year_mon = '03'
    year = int(year_mon[:4])
    print year
    d1 = {
        '1':23
    }
    d2 = {
        1:23
    }
    d3 = dict(d1, **d2)
    print d3