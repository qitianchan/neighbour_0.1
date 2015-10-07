# # -*- coding: utf-8 -*-
from neighbour.extensions import db
from neighbour.utils.database import CRUDMixin


class Tenant(db.Model, CRUDMixin):
    __tablename__ = 'tenant'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tenant_type = db.Column(db.Integer)
    name = db.Column(db.VARCHAR(128))
    phone = db.Column(db.Integer)
    house_info_id = db.Column(db.Integer, db.ForeignKey('house_info.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @classmethod
    def get_tenants(cls, house_info_id):
        """
        获取所有住户
        :param house_info_id:
        :return:
        """
        return cls.query.filter(cls.house_info_id == house_info_id).all()

    @classmethod
    def delete_tenants(cls,tenant_id):
        cls.query.filter(cls.id == tenant_id).delete()
        db.session.commit()



