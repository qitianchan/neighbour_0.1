# -*- coding: utf-8 -*-
from neighbour.extensions import db
from neighbour.utils.database import CRUDMixin


class Cell(db.Model, CRUDMixin):
    __tablename__ = 'cell'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    residential_area_id = db.Column(db.Integer, db.ForeignKey('residential_areas.id'))
    cell_name = db.Column(db.String(255))

    # one-to-many
    buildings = db.relationship('Building',
                                     backref='cell',
                                     primaryjoin='Building.cell_id == Cell.id')
