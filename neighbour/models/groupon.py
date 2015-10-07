# # -*- coding: utf-8 -*-
from neighbour.extensions import db
from neighbour.utils.database import CRUDMixin

class GrouponOrderAreaOccocs(db.Model, CRUDMixin):
    __tablename__ = 'groupon_order_area_accocs'
    residential_area_id = db.Column(db.Integer, db.ForeignKey('residential_areas.id'), primary_key=True)
    groupon_order_id = db.Column(db.Integer, db.ForeignKey('groupon_order.id'), primary_key=True)
    residential_area = db.relationship('ResidentialAreas', backref="groupon_order_area_accocs")

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
    profile_img = db.Column(db.String(512))

    orders = db.relationship('GrouponOrder', backref='groupon')
    residential_areas = db.relationship('GrouponOrderAreaOccocs',backref='groupon')

