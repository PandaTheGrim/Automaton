import os

class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = 'VERY_SAFE_SECRET'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True