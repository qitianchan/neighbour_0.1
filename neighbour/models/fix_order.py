# -*- coding: utf-8 -*-
from neighbour.extensions import db
from neighbour.utils.database import CRUDMixin


class FixOrder(db.Model, CRUDMixin):
    __tablename__ = 'fix_order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    house_info_id = db.Column(db.Integer, db.ForeignKey('house_info.id'))
    problem = db.Column(db.VARCHAR(1000))
    time = db.Column(db.VARCHAR(512))
    create_time = db.Column(db.Integer)
    confirm_time = db.Column(db.Integer)
    done_time = db.Column(db.Integer)
    status = db.Column(db.SmallInteger)

    imgs = db.relationship('FixOrderImg', backref='fix_order',
                           cascade="all, delete-orphan", passive_deletes=True,
                           primaryjoin='FixOrderImg.fix_order_id == FixOrder.id')

