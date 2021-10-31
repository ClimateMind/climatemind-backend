from flask import abort
import os
import urllib
from datetime import timedelta

from app.network_x_tools.network_x_processor import network_x_processor


class BaseConfig(object):
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "DEFAULT_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=14)
    JWT_ACCESS_COOKIE_NAME = "access_token"
    JWT_REFRESH_COOKIE_NAME = "refresh_token"
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_REFRESH_COOKIE_PATH = "/refresh"
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_SAMESITE = None
    CACHE_TYPE = "simple"

    DB_CREDENTIALS = os.environ.get("DATABASE_PARAMS")
    SQLALCHEMY_DATABASE_URI = (
        "mssql+pyodbc:///?odbc_connect=%s" % urllib.parse.quote_plus(DB_CREDENTIALS)
    )

    nx_processor = network_x_processor()
    G = nx_processor.get_graph()


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    # todo: add mock mind here
