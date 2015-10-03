# # -*- coding: utf-8 -*-
# from neighbour.extensions import db
# from neighbour.utils.database import CRUDMixin
#
# # 商品图片
# class ProductImage(db.Model, CRUDMixin):
#     __tablename__ = 't_product_img'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     product_id = db.Column(db.Integer, db.ForeignKey('t_product.id'))
#     img_url = db.Column(db.String(512))
#     order = db.Column(db.SmallInteger)
#
#
