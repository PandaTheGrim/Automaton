import os

class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = 'VERY_SAFE_SECRET'
    POSTGRESQL_DATABASE_DATABASE = 'automaton'
    POSTGRESQL_DATABASE_USERNAME = 'automaton'
    POSTGRESQL_DATABASE_PASSWORD = 'automaton'
    POSTGRESQL_DATABASE_HOSTNAME = 'localhost'
    POSTGRESQL_DATABASE_PORTNUMB = '5433'
    SQLALCHEMY_DATABASE_URI = 'postgresql://{usrn}:{pasw}@{host}:{port}/{db_n}'.format(
        usrn=POSTGRESQL_DATABASE_USERNAME,
        pasw=POSTGRESQL_DATABASE_PASSWORD,
        host=POSTGRESQL_DATABASE_HOSTNAME,
        port=POSTGRESQL_DATABASE_PORTNUMB,
        db_n=POSTGRESQL_DATABASE_DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    AUTOMATON_FILES_DIR = '/var/automaton'
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'admin'
    ADMIN_EMAIL = 'admin@test.test'

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True