from flask import abort
import os
import urllib

from knowledge_graph.Mind import Mind


class BaseConfig(object):
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True

    # Temporary
    # basedir = os.path.abspath(os.path.dirname(__file__))
    # SQLALCHEMY_DATABASE_URI = #"sqlite:///" + os.path.join(basedir, "app.db")
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # DATABASE_PARAMS = os.environ["DATABASE_PARAMS"]
    # SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % DATABASE_PARAMS
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_TYPE = "simple"

    DB_CREDENTIALS = os.environ.get("DATABASE_PARAMS")
    SQLALCHEMY_DATABASE_URI = (
        "mssql+pyodbc:///?odbc_connect=%s" % urllib.parse.quote_plus(DB_CREDENTIALS)
    )
    # SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("%", "%%")

    # End Temporary

    try:
        MIND = Mind()
    except (FileNotFoundError, IsADirectoryError, ValueError):
        abort(404)


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    # todo: add mock mind here
