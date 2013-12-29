# -*- config:utf-8 -*-

from os import environ as ENV
import logging
from datetime import timedelta

DEFAULT_ENV = 'development'
APP_ENV = ENV.get('APP_ENV', DEFAULT_ENV)
default_db = 'sqlite:///../%s.db' % APP_ENV
redis_url = ENV.get('REDISTOGO_URL', 'redis://localhost:6379/10')


class BaseConfig(object):
    # App environment name (eg. development|production|test|staging)
    APP_ENV = APP_ENV

    # use DEBUG mode?
    DEBUG = False

    # use TESTING mode?
    TESTING = False

    # use server x-sendfile?
    USE_X_SENDFILE = False

    # RQ (Delayed jobs)
    RQ_DEFAULT_URL = redis_url

    # Caching
    CACHE_REDIS_URL = redis_url
    if 'production' == APP_ENV:
        CACHE_TYPE = 'redis'
    else:
        CACHE_TYPE = 'null'

    # DATABASE CONFIGURATION
    SQLALCHEMY_DATABASE_URI = ENV.get('DATABASE_URL', default_db)
    SQLALCHEMY_ECHO = False

    CSRF_ENABLED = True
    SECRET_KEY = 'secret'  # import os; os.urandom(24)

    # LOGGING
    LOGGER_NAME = 'server_log'
    LOG_FILENAME = 'server.log'
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = '%(asctime)s %(levelname)s\t: %(message)s'  # used by logging.Formatter

    PERMANENT_SESSION_LIFETIME = timedelta(days=1)

    # EMAIL CONFIGURATION
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_DEBUG = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    DEFAULT_MAIL_SENDER = 'example@server.com'

    # see example/ for reference
    # ex: BLUEPRINTS = ['blog.app']  # where app is a Blueprint instance
    # ex: BLUEPRINTS = [('blog.app', '/myblog')]  # where app is a Blueprint instance
    # ex: BLUEPRINTS = [('blog.app', {'url_prefix': '/myblog'})]  # where app is a Blueprint instance
    BLUEPRINTS = []


class production(BaseConfig):
    pass


class development(BaseConfig):
    DEBUG = True
    MAIL_DEBUG = True
    SQLALCHEMY_ECHO = True


class test(BaseConfig):
    TESTING = True
    CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_ECHO = False
    CACHE_NO_NULL_WARNING = True
