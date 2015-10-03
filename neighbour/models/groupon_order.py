# # -*- coding: utf-8 -*-
# from neighbour.extensions import db
# from neighbour.utils.database import CRUDMixin
#
#
# class GrouponOrder(db.Model, CRUDMixin):
#     __tablename__ = 'groupon_order'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     groupon_id = db.Column(db.Integer, db.ForeignKey('groupon.id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     # tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'))
#     residential_area_id = db.Column(db.Integer, db.ForeignKey('residential_areas.id'))
#     create_time = db.Column(db.Integer)                                                 # 创建时间
#     paid_time = db.Column(db.Integer)                                                   # 付款时间
#     order_status = db.Column(db.SMALLINT)                                               # 订单状态
#
#     # 订单冗余信息
#     user_phone = db.Column(db.VARCHAR(128))                                           # 手机
#     user_name = db.Column(db.VARCHAR(128))                                            # 联系人
#     groupon_title = db.Column(db.VARCHAR(512))
#     groupon_price = db.Column(db.Integer)
#     product_title = db.Column(db.VARCHAR(512))
#     product_original_price = db.Column(db.Integer)
#     product_type = db.Column(db.Integer)
#     area_name = db.Column(db.VARCHAR(512))
#     area_province = db.Column(db.VARCHAR(32))
#     area_city = db.Column(db.VARCHAR(32))
#     area_zone = db.Column(db.VARCHAR(32))
#     area_stree = db.Column(db.VARCHAR(512))
#
#     orders = db.relationship('GrouponOrder', backref='groupon', primaryjoin='GrouponOrder.groupon_id == Groupon.id')
#
#     residential_areas = db.relationship('GrouponResidentialAreas',
#                                         backref='groupon',
#                                         primaryjoin='GroupResidentialAreas.groupon_id == Groupon.id')
#
