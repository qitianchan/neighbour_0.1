# # -*- coding: utf-8 -*-
from neighbour.extensions import db
from neighbour.models.residential_areas import ResidentialAreas
from neighbour.utils.database import CRUDMixin



class GrouponOrder(db.Model, CRUDMixin):
    __tablename__ = 'groupon_order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    groupon_id = db.Column(db.Integer, db.ForeignKey('groupon.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'))
    residential_area_id = db.Column(db.Integer, db.ForeignKey('residential_areas.id'))
    create_time = db.Column(db.Integer)                                                 # 创建时间
    paid_time = db.Column(db.Integer)                                                   # 付款时间
    confirm_time = db.Column(db.Integer)                                                # 受理时间
    order_status = db.Column(db.SMALLINT)                                               # 订单状态

    # 订单冗余信息
    user_phone = db.Column(db.VARCHAR(128))                                           # 手机
    user_name = db.Column(db.VARCHAR(128))                                            # 联系人
    groupon_title = db.Column(db.VARCHAR(512))
    groupon_price = db.Column(db.Integer)
    count = db.Column(db.Integer)
    total_fee = db.Column(db.Integer)
    product_title = db.Column(db.VARCHAR(512))
    product_original_price = db.Column(db.Integer)
    product_type = db.Column(db.Integer)
    area_name = db.Column(db.VARCHAR(512))
    area_province = db.Column(db.VARCHAR(32))
    area_city = db.Column(db.VARCHAR(32))
    area_zone = db.Column(db.VARCHAR(32))
    area_stree = db.Column(db.VARCHAR(512))

    user = db.relationship('User', backref='groupon_orders')

    @classmethod
    def get_orders_by_status_user(cls, status, user_id, page=1, page_count=20):
        data = cls.query.filter(cls.user_id == user_id, cls.order_status == status).paginate(page, page_count).items
        return data

    @classmethod
    def get_groupon_order_by_id(cls, order_id):
        data = cls.query.filter(cls.id == order_id).first()
        return data

