# # -*- coding: utf-8 -*-
# from neighbour.extensions import db
# from neighbour.utils.database import CRUDMixin
#
#
# class HouseFee(db.Model, CRUDMixin):
#     __tablename__ = 'house_fee'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     house_info_id = db.Column(db.Integer, db.ForeignKey('house_info.id'))
#     year = db.Column(db.Integer)
#     month = db.Column(db.Integer)
#     water_num = db.Column(db.Float)
#     water_fee = db.Column(db.Integer)
#     electricity = db.Column(db.Float)
#     electricity_fee = db.Column(db.Integer)