from flask import abort
import os
import urllib

from knowledge_graph.Mind import Mind


class BaseConfig(object):
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_TYPE = "simple"

    DB_CREDENTIALS = os.environ.get("DATABASE_PARAMS")
    SQLALCHEMY_DATABASE_URI = (
        "mssql+pyodbc:///?odbc_connect=%s" % urllib.parse.quote_plus(DB_CREDENTIALS)
    )

class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    # todo: add mock mind here
