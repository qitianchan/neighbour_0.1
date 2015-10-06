# -*- coding: utf-8 -*-
from neighbour.extensions import db
from neighbour.utils.database import CRUDMixin
from neighbour.models.tenant import Tenant
from neighbour.models.house_fee import HouseFee
from sqlalchemy import and_


# 多对应  中间表
# user_house_table = db.Table('user_house_table',
#                             db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#                             db.Column('house_info_id', db.Integer, db.ForeignKey('house_info.id')),
#                             db.Column('user_type', db.Integer)
#                             )


class UserHouseTable(db.Model, CRUDMixin):
    __tablename__ = 'user_house_table'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    house_info_id = db.Column(db.Integer, db.ForeignKey('house_info.id'), primary_key=True)
    user_type = db.Column(db.Integer)
    user = db.relationship('User', backref="house_accocs")

    @classmethod
    def get_user_house(cls, user_id, house_info_id):
        """
        根据user_id和house_info_id获取关联信息项
        :param user_id: 用户id
        :param house_info_id:
        :return:关联项
        """
        return cls.query.filter(and_(cls.user_id==user_id, cls.house_info_id==house_info_id)).first()


class HouseInfo(db.Model, CRUDMixin):
    __tablename__ = 'house_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_number = db.Column(db.VARCHAR(12))
    owner = db.Column(db.VARCHAR(255))
    owner_phone = db.Column(db.VARCHAR(255))
    property_management_fee = db.Column(db.Integer)
    tv_fee = db.Column(db.Integer)

    users = db.relationship('UserHouseTable', backref="house")

    tenants = db.relationship('Tenant',
                                  backref="house",
                                  primaryjoin="Tenant.house_info_id == HouseInfo.id"
                            )
    house_fees = db.relationship('HouseFee', backref='house_info', primaryjoin='HouseFee.house_info_id == HouseInfo.id')

    # fix_orders = db.relationship('FixOrder', backref='house_info', primaryjoin='FixOrder.house_info_id == HouseInfo.id')

    # valiate_infos = db.relationship('ValiateInfo', backref='house_info',
    #                                 primaryjoin='ValiateInfo.house_info_id == HouseInfo.id')

    # users = db.relationship('User', backref=db.backref('house_infos', lazy='dynamic'), secondary=user_house_table)

