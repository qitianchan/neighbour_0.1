# -*- coding: utf-8 -*-
from flask import Blueprint

fees = Blueprint('fees', __name__)


@fees.route('/set_water_num', methods=['GET', 'POST'])
def set_water_num():
    """
    设置水表读数
    :return: 这个月的水费
    """
    water_fee = 0

    return water_fee
