# -*- coding: utf-8 -*-
from neighbour.extensions import db
from neighbour.utils.database import CRUDMixin


class Notice(db.Model, CRUDMixin):
    """
        信息通知，微信图文消息类型
    """
    __tablename__ = 'notice'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    deadline= db.Column(db.Integer)
    create_time= db.Column(db.Integer)
    title = db.Column(db.VARCHAR(128))
    info = db.Column(db.TEXT)
    picurl= db.Column(db.TEXT)
    status = db.Column(db.Integer)
    residential_area_id = db.Column(db.Integer, db.ForeignKey('residential_areas.id'))

