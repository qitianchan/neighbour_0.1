# -*- coding: utf-8 -*-
from neighbour.extensions import db
from neighbour.utils.database import CRUDMixin
from hashlib import sha1
from neighbour.utils.helper import create_salt
from neighbour.models.tenant import Tenant

class User(db.Model, CRUDMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # residential_area_id = db.Column(db.Integer, db.ForeignKey('residential_areas.id'))
    # house_info_id = db.Column(db.Integer, db.ForeignKey('house_info.id'))
    login_name = db.Column(db.String(127))
    password = db.Column(db.VARCHAR(127))
    salt = db.Column(db.VARCHAR(127))
    wechat_nickname = db.Column(db.String(127))
    wechat_openid = db.Column(db.String(255))
    user_type = db.Column(db.Integer)
    phone = db.Column(db.VARCHAR(15))
    roles = db.Column(db.Integer)
    status = db.Column(db.SmallInteger)

    tenants = db.relationship('Tenant',
                              backref="user",
                              primaryjoin="Tenant.user_id == User.id"
                              )
    # groupon_orders = db.relationship('GrouponOrder',
    #                                  backref='user',
    #                                  primaryjoin='GrouponOrder.user_id == User.id')
    #
    # valiate_infos = db.relationship('ValiateInfo',
    #                                     backref='user',
    #                                     primaryjoin='ValiateInfo.user_id == User.id')

    @classmethod
    def get_user_by_openid(cls, openid):
        """
        通过openid获取用户
        :param openid: 微信openid
        :return: 对应的用户
        """
        return cls.query.filter_by(wechat_openid=openid).first()

    def check_password(self, password):
        """Check passwords. If passwords match it returns true, else false"""

        if self.password is None:
            return False

        sha1_obj = sha1()
        sha1_obj.update(password+self.salt)

        return self.password == sha1_obj.hexdigest()


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python
