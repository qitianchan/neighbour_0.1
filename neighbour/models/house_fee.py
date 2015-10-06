# # -*- coding: utf-8 -*-
from neighbour.extensions import db
from neighbour.utils.database import CRUDMixin
import time
from sqlalchemy import and_, or_

class HouseFee(db.Model, CRUDMixin):
    __tablename__ = 'house_fee'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    house_info_id = db.Column(db.Integer, db.ForeignKey('house_info.id'))
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    water_num = db.Column(db.Float, default=0)
    water_fee = db.Column(db.Integer, default=0)
    water_fee_status = db.Column(db.Integer, default=0)
    gas_num = db.Column(db.Float, default=0)
    gas_fee = db.Column(db.Integer, default=0)
    gas_fee_status = db.Column(db.Integer, default=0)
    electricity_num = db.Column(db.Float,default=0)
    electricity_fee = db.Column(db.Integer, default=0)
    electricity_fee_status = db.Column(db.Integer, default=0)
    status = db.Column(db.Integer)

    @classmethod
    def get_last_mon_fee(cls, house_info_id):
        """
        获取当前的上个月费用
        :param house_info_id:
        :return:
        """
        time_struct = time.localtime()
        year = time_struct.tm_year
        mon = time_struct.tm_mon - 1
        if(mon < 1):
            year -= 1

        fee = cls.query.filter(and_(cls.house_info_id == house_info_id,
                                    cls.year == year,
                                    cls.month == mon
                                    )).first()
        return fee

    @classmethod
    def get_year_fees(cls, house_info_id, year=None):
        """
        获取指定年分的费用，如果year未指出，则为当年
        :param house_info_id:
        :param year: 指定年份
        :return:
        """
        if not year:
            year = time.localtime().tm_year

        fees = cls.query.filter(and_(
            cls.house_info_id == house_info_id,
            cls.year == year
        )).all()

        return fees


    @classmethod
    def get_house_fees(cls, house_info_id, monList):
        """
        获取多个月份的费用
        :param house_info_id:
        :param monList: 时间列表[{'year': 2015, 'mon': 9}, {'year':2015, 'mon':10}]
        :return:
        """
        print monList
        if not monList:
           current_time = time.time()
           year = current_time.tm_year
           mon = current_time.tm_mon - 1


        fees = cls.query.filter(and_(
            cls.house_info_id == house_info_id,
            or_(and_(
                    cls.year == year_mon['year'],
                    cls.month == year_mon['mon']
                )for year_mon in monList,
            )
        )).all()

        return fees

