# -*- coding: utf-8 -*-
from neighbour.extensions import db
from neighbour.utils.database import CRUDMixin


class FixOrderImg(db.Model, CRUDMixin):
    __tablename__ = 'fix_order_img'
    img_name = db.Column(db.VARCHAR(255), primary_key=True)
    fix_order_id = db.Column(db.Integer, db.ForeignKey('fix_order.id', ondelete='CASCADE'))

