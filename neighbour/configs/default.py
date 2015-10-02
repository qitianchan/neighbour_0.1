# -*- coding: utf-8 -*-


class DefaultConfig(object):
    DEBUG = True
    TESTING = False

    SEND_LOG = False
    # URI用”mysql://username:password@localhost/database?charset=utf8&use_unicode=0″
    # 这种格式可以解决中文英文混合返回utf8编码的问题，不报UnicodeDecodeError错误
    SQLALCHEMY_DATABASE_URI = 'mysql://root:aaaaaa@localhost/test'
    # SQLALCHEMY_DATABASE_URI = 'mysql://cheaboar:Wind1748@wind1748.mysql.rds.aliyuncs.com/cheaboar?charset=utf8&use_unicode=0'

    # This will print all SQL statements
    SQLALCHEMY_ECHO = True

    # Security
    # This is the secret key that is used for session signing.
    # You can generate a secure key with os.urandom(24)
    SECRET_KEY = 'secret key'

    # Protection against form post fraud
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = "reallyhardtoguess"