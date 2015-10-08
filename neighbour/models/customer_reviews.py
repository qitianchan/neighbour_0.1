# -*- coding: utf-8 -*-
from neighbour.extensions import db
from neighbour.utils.database import CRUDMixin
from sqlalchemy.sql import func

class CustomerReviews(db.Model, CRUDMixin):
    __tablename__ = 'customer_reviews'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    groupon_id = db.Column(db.Integer, db.ForeignKey('groupon.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score = db.Column(db.SmallInteger)
    create_time = db.Column(db.Integer)                                                 # 创建时间
    content = db.Column(db.VARCHAR(1024))

    @classmethod
    def get_statics_data(cls, groupon_id):
        data = db.session.query(func.avg(cls.score).label('avg_score'),
                               func.count(cls.groupon_id).label('reviews_count')
                               ).filter(cls.groupon_id == groupon_id).first()
        name = ('avg_score', 'reviews_count')
        return dict(zip(name, data))
