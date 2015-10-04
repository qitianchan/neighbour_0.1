# -*- coding: utf-8 -*-
from neighbour.models.residential_areas import ResidentialAreas
from flask import Blueprint, jsonify


wechat_front = Blueprint('wechat_front', __name__)


@wechat_front.route('/get_areas', methods=['GET'])
def get_areas():
    residential_areas = ResidentialAreas.get_areas()
    result = {}

    for r in residential_areas:
        if result.has_key(r.zone_id):
            result[r.zone_id]['areaList'].append({
                'areaID': r.id,
                'areaName' : r.area_name
            })
        else:
            result[r.zone_id] = {
                'zoneID': r.zone_id,
                'zoneName' : r.zone.area_name,
                'areaList' : [{
                    'areaID' : r.id,
                    'areaName' : r.area_name
                }]
            }
    data = list()
    for key in result.keys():
        data.append(result[key])

    final_return = {
        'retCode' : '0000',
        'retMsg' : '',
        'zoneList' : data
    }

    return jsonify(final_return)

