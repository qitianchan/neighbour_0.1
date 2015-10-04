# -*- coding: utf-8 -*-
from neighbour.extensions import db
from neighbour.utils.database import CRUDMixin
from neighbour.models.areas import Areas
from neighbour.models.cell import Cell

# groupon_residential_ereas = db.Table('groupon_residential_ereas',
#                                      db.Column('residential_area_id', db.Integer, db.ForeignKey('residential_areas.id'))
#                                      , db.Column('groupon_id', db.Integer, db.ForeignKey('groupon.id')),
#                                      )


class ResidentialAreas(db.Model, CRUDMixin):
    __tablename__ = 'residential_areas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    area_name = db.Column(db.VARCHAR(255))
    stree = db.Column(db.VARCHAR(512))
    person_in_charge = db.Column(db.VARCHAR(64))
    contact_phone = db.Column(db.VARCHAR(15))
    # province_id = db.Column(db.Integer, db.ForeignKey('areas.id'))
    # city_id = db.Column(db.Integer, db.ForeignKey('areas.id'))
    zone_id = db.Column(db.Integer, db.ForeignKey('areas.id'))
    status = db.Column(db.SMALLINT)

    # notices = db.relationship('Notice', backref='residential_area',
    #                           primaryjoin='Notice.residential_area_id == ResidentialAreas.id')
    #
    # infos = db.relationship('Info', backref='residential_area',
    #                           primaryjoin='Info.residential_area_id == ResidentialAreas.id')
    #
    # groupon_oders = db.relationship('GrouponOrder', backref='residential_area',
    #                           primaryjoin='GrouponOrder.residential_area_id == ResidentialAreas.id')
    #
    # users = db.relationship('User', backref='residential_area',
    #                           primaryjoin='User.residential_area_id == ResidentialAreas.id')
    #
    cells = db.relationship('Cell', backref='residential_area',
                              primaryjoin='Cell.residential_area_id == ResidentialAreas.id')
    #
    # province = db.relationship('Areas')
    # city = db.relationship('Areas')
    zone = db.relationship('Areas', backref="residential_areas")
    #
    # groupons = db.relationship('Groupon', secondary=groupon_residential_ereas,
    #                            backref=db.backref('residential_areas', lazy='dynamic'))

    @classmethod
    def get_areas(self):
        """
        返回所有的小区
        :return:
        """
        return self.query.all()

    @classmethod
    def get_area_info(self, area_id):
        """
        获取小区所有
        :param area_id:小区id
        :return:
        """
        area = self.query.filter(self.id == area_id).first()
        data = None
        if area:
            data = {
                'code': area_id,
                'name': area.area_name,
                'cellList': [
                    {
                        'cellID': cell.id,
                        'cellName': cell.cell_name,
                        'buildingList': [
                            {
                                'buildingID': building.id,
                                'buildingName': building.building_name,
                                'houseList': [
                                    {
                                        'houseID': house.id,
                                        'houseCode': house.room_number
                                    }for house in building.house_infos
                                ]
                            }for building in cell.buildings
                        ]
                    }for cell in area.cells
                ]
            }

        return data

# data = {
#     'code': 131,
#     'name': 'das',
#     'buildingList':[
#         {
#             'buildingCode':23,
#             'buildingName':'sdss',
#             'houseList': [
#                 {
#                     'houseNum' : 232,
#                     'houseCode':'2323'
#                 },
#                 {
#                     'houseNum' : 232,
#                     'houseCode':'2323'
#                 }
#             ]
#         },
#         {
#             'buildingCode':23,
#             'buildingName':'sdss',
#             'houseList': [
#                 {
#                     'houseNum' : 232,
#                     'houseCode':'2323'
#                 },
#                 {
#                     'houseNum' : 232,
#                     'houseCode':'2323'
#                 }
#             ]
#         }
#     ]
# }

