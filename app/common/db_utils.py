import os
import urllib

from sqlalchemy import create_engine


def create_sqlalchemy_engine(**kwargs):
    DB_CREDENTIALS = os.environ.get("DATABASE_PARAMS")
    SQLALCHEMY_DATABASE_URI = (
        "mssql+pyodbc:///?odbc_connect=%s" % urllib.parse.quote_plus(DB_CREDENTIALS)
    )
    return create_engine(SQLALCHEMY_DATABASE_URI, **kwargs)
