# -*- coding: utf-8 -*-
from neighbour.extensions import db
from neighbour.utils.database import CRUDMixin


class HouseInfo(db.Model, CRUDMixin):
    __tablename__ = 'house_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    property_management_fee = db.Column(db.Integer)
    tv_fee = db.Column(db.Integer)

    house_fees = db.relationship('HouseFee', backref='house_info', primaryjoin='HouseFee.house_info_id == HouseInfo.id')

    fix_orders = db.relationship('FixOrder', backref='house_info', primaryjoin='FixOrder.house_info_id == HouseInfo.id')

    valiate_infos = db.relationship('ValiateInfo', backref='house_info', primaryjoin='ValiateInfo.house_info_id == HouseInfo.id')

    users = db.relationship('User',backref='house_info',
                             primaryjoin='User.house_info_id == HouseInfo.id')
