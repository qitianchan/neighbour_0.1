# -*- coding: utf-8 -*-
from neighbour.extensions import db
from neighbour.utils.database import CRUDMixin

class User(db.Model, CRUDMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    residential_area_id = db.Column(db.Integer, db.ForeignKey('residential_areas.id'))
    login_name = db.Column(db.String(127))
    password = db.Column(db.TEXT)
    wechat_nickname = db.Column(db.String(127))
    wechat_openid = db.Column(db.String(255))
    user_type = db.Column(db.Integer)
    phone = db.Column(db.VARCHAR(15))
    status = db.Column(db.SmallInteger)

    # 订单转在tenant表关系中
    # groupon_orders = db.relationship('GrouponOrder',
    #                                  backref='user',
    #                                  primaryjoin='GrouponOrder.user_id == User.id')

    valiate_infos = db.relationship('ValiateInfo',
                                        backref='user',
                                        primaryjoin='ValiateInfo.user_id == User.id')
    house_infos =  db.relationship('HouseInfo',
                                   backref='user',
                                   primaryjoin='HouseInfo.user_id == User.id')
