# -*- coding: utf-8 -*-
from neighbour.extensions import db
from neighbour.utils.database import CRUDMixin


class ValiateInfo(db.Model, CRUDMixin):
    __tablename__ = 'valiate_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    house_info_id = db.Column(db.Integer, db.ForeignKey('house_info.id'))
    user_type = db.Column(db.Integer)
    user_name = db.Column(db.String(127))
    user_phone = db.Column(db.String(255))
    create_time = db.Column(db.Integer)
    status = db.Column(db.SmallInteger)

    groupon_orders = db.relationship('GrouponOrder',
                                     backref='user',
                                     primaryjoin='GrouponOrder.user_id == User.id')