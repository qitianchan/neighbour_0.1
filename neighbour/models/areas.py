# # -*- coding: utf-8 -*-
# from neighbour.extensions import db
# from neighbour.utils.database import CRUDMixin
#
#
# class Areas(db.Model, CRUDMixin):
#     """
#         消息，用于通知小区管理员的消息
#     """
#     __tablename__ = 'areas'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     area_name = db.Column(db.VARCHAR(128))                                                                #标识消息状态是否已读
#     parent_id = db.Column(db.Integer)
#
