from flask import abort
import os
import urllib.parse

from knowledge_graph.Mind import Mind

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    DEBUG = False
    
    # Changing for Azure
    params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:sql-web-prod-001.database.windows.net,1433;DATABASE=sqldb-web-prod-001;UID=sqlSvc;PWD=Pxwvhlje3654dwx!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    #SQLALCHEMY_DATABASE_URI = os.environ.get(
    #    "DATABASE_URL"
    #) or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # End changing for Azure
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True

    try:
        MIND = Mind()
    except (FileNotFoundError, IsADirectoryError, ValueError):
        abort(404)


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    # todo: add mock mind here
