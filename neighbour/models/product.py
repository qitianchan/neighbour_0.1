# # -*- coding: utf-8 -*-
from neighbour.extensions import db
from neighbour.utils.database import CRUDMixin


# 商品
class Product(db.Model, CRUDMixin):
    __tablename__ = 't_product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.TEXT)
    orginal_price = db.Column(db.DECIMAL)
    category = db.Column(db.Integer)
    status = db.Column(db.SMALLINT)
    create_time = db.Column(db.Integer)

    # one-to-many
    images = db.relationship('ProductImage',
                             backref='product',
                             primaryjoin='ProductImage.product_id == Product.id',
                             cascade="all, delete-orphan")

    groupons = db.relationship('Groupon',
                               backref='product',
                               primaryjoin='Groupon.id == Product.id')


