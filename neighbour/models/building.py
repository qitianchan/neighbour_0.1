# # -*- coding: utf-8 -*-
# from neighbour.extensions import db
# from neighbour.utils.database import CRUDMixin
#
#
# class Building(db.Model, CRUDMixin):
#     __tablename__ = 'building'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     cell_id = db.Column(db.Integer, db.ForeignKey('cell.id'))
#     building_name = db.Column(db.String(255))
#
#     # one-to-many
#     house_infos = db.relationship('HouseInfo',
#                                      backref='building',
#                                      primaryjoin='HouseInfo.building_id == Building.id')
