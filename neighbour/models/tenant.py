# -*- coding: utf-8 -*-
from neighbour.extensions import db
from neighbour.utils.database import CRUDMixin


class Tenant(db.Model, CRUDMixin):
    __tablename__ = 'tenant'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tenant_type = db.Column(db.Integer)
    name = db.Column(db.VARCHAR(128))
    phone = db.Column(db.Integer)
    house_info_id = db.Column(db.Integer, db.ForeignKey('house_info.id'))

    groupon_orders = db.relationship('GrouponOrder',
                                     backref='tenant',
                                     primaryjoin='GrouponOrder.tenant_id == Tenant.id')
