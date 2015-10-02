# -*- coding: utf-8 -*-
from neighbour.extensions import db
from neighbour.utils.database import CRUDMixin


class Info(db.Model, CRUDMixin):
    """
        消息，用于通知小区管理员的消息
    """
    __tablename__ = 'info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.TEXT)
    create_time = db.Column(db.Integer)
    status = db.Column(db.Integer)                                                                  #标识消息状态是否已读
    residential_area_id = db.Column(db.Integer, db.ForeignKey('residential_areas.id'))

