import pyodbc
from sqlalchemy import create_engine
import os
import urllib


DB_CREDENTIALS = os.environ.get("DATABASE_PARAMS")
SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % urllib.parse.quote_plus(
    DB_CREDENTIALS
)

with create_engine(
    SQLALCHEMY_DATABASE_URI, isolation_level="AUTOCOMMIT", echo=True
).connect() as connection:
    connection.execute("CREATE DATABASE [sqldb-web-prod-001]")
