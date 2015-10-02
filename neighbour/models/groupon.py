# -*- coding: utf-8 -*-
from neighbour.extensions import db
from neighbour.utils.database import CRUDMixin


class Groupon(db.Model, CRUDMixin):
    __tablename__ = 'groupon'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer)
    create_time = db.Column(db.Integer)
    begin_time = db.Column(db.Integer)
    end_time = db.Column(db.Integer)
    title = db.Column(db.String(255))
    groupon_price = db.Column(db.Integer)
    groupon_status = db.Column(db.Integer)

    orders = db.relationship('GrouponOrder',
                                     backref='groupon',
                                     primaryjoin='GrouponOrder.groupon_id == Groupon.id')

    residential_areas = db.relationship('GrouponResidentialAreas',
                                        backref='groupon',
                                        primaryjoin='GroupResidentialAreas.groupon_id == Groupon.id')

