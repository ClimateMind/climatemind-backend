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

    JWT_COOKIE_SECURE = False
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    # TODO Change for production & use env variable.
    JWT_SECRET_KEY = "super-secret"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_ACCESS_COOKIE_NAME = "access_token"
    JWT_REFRESH_COOKIE_NAME = "refresh_token"
    JWT_COOKIE_CSRF_PROTECT = False
    # JWT_REFRESH_COOKIE_PATH = "/refresh"
    CACHE_TYPE = "simple"

    DB_CREDENTIALS = os.environ.get("DATABASE_PARAMS")
    SQLALCHEMY_DATABASE_URI = (
        "mssql+pyodbc:///?odbc_connect=%s" % urllib.parse.quote_plus(DB_CREDENTIALS)
    )

    try:
        nx_processor = network_x_processor()
        G = nx_processor.get_graph()
    except:
        print(
            """No Pickle File Exists, Please run Process_New_Ontology.py
                    If you are processing the ontology, disregard this message"""
        )


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    # todo: add mock mind here
