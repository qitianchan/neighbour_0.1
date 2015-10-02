# -*- coding: utf-8 -*-
from flask import Flask
from district.views import distric
from district.valiation import valiation_app
from wechat.navbar import wechat_navbar
from extensions import db


def create_app(config=None):
    """
    Creates the app
    :param config:
    :return:
    """
    app = Flask(__name__)
    # Use the default config and override it afterwards
    app.config.from_object('neighbour.configs.default.DefaultConfig')
    # Update the config
    app.config.from_object(config)

    configure_blueprint(app)
    configure_extensions(app)
    app.debug = app.config['DEBUG']
    return app


def configure_blueprint(app):
    app.register_blueprint(distric)
    app.register_blueprint(valiation_app)
    app.register_blueprint(wechat_navbar)


def configure_extensions(app):
    # Flask-SQLAlchemy
    db.init_app(app)
    db.app = app

if __name__ == '__main__':
    app = create_app()
    from neighbour.models.groupon import Groupon
    from neighbour.models.groupon_order import GrouponOrder
    from neighbour.models.groupon import Groupon
    from neighbour.models.groupon_order import GrouponOrder
    from neighbour.models.house_info import HouseInfo
    from neighbour.models.valiate_info import ValiateInfo
    from neighbour.models.user import User
    from neighbour.models.fix_order import FixOrder
    from neighbour.models.house_fee import HouseFee
    from neighbour.models.building import Building
    from neighbour.models.cell import Cell
    from neighbour.models.residential_areas import ResidentialAreas
    from neighbour.models.notice import Notice
    from neighbour.models.info import Info
    from neighbour.models.areas import Areas
    from neighbour.models.tenant import Tenant


    db.drop_all()
    db.create_all()


