# -*- coding: utf-8 -*-
from flask import Flask
from neighbour.district.views import distric
from neighbour.wechat.navbar import wechat_navbar
from neighbour.extensions import db, login_manager
from neighbour.views.account import account
from neighbour.views.test import test
from neighbour.views.wechat import wechat
from neighbour.controller.wechat_api import wechat_front
from neighbour.models.product import Product
from neighbour.models.product_image import ProductImage
from neighbour.models.groupon_order import GrouponOrder
from neighbour.models.groupon import GrouponOrderAreaOccocs
from neighbour.models.groupon import Groupon
from neighbour.models.house_info import HouseInfo
from neighbour.models.customer_reviews import CustomerReviews
# from neighbour.models.valiate_info import ValiateInfo
from neighbour.models.user import User
# from neighbour.models.fix_order import FixOrder
from neighbour.models.house_fee import HouseFee
from neighbour.models.building import Building
from neighbour.models.cell import Cell
from neighbour.models.areas import Areas
from neighbour.models.residential_areas import ResidentialAreas
# from neighbour.models.notice import Notice
# from neighbour.models.info import Info
from neighbour.models.tenant import Tenant

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
    app.register_blueprint(wechat_navbar)
    app.register_blueprint(account, url_prefix=app.config['ACCOUNT_URL_PREFIX'])
    app.register_blueprint(test, url_prefix=app.config['TEST_URL_PREFIX'])
    app.register_blueprint(wechat, url_prefix=app.config['WECHAT_URL_PREFIX'])
    app.register_blueprint(wechat_front, url_prefix=app.config['WECHAT_FRONT_URL_PREFIX'])

def configure_extensions(app):
    # Flask-SQLAlchemy
    db.init_app(app)
    db.app = app

    #Flask-Login
    login_configure(app)


def login_configure(app):
    login_manager.init_app(app)
    login_manager.login_view = app.config['LOGIN_VIEW']

    @login_manager.user_loader
    def load_user(user_id):
        user_instance = User.query.filter_by(id=user_id).first()
        if user_instance:
            return user_instance
        else:
            return None



if __name__ == '__main__':
    app = create_app()



    # db.drop_all()
    db.create_all()


