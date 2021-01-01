import pandas as pd
from sqlalchemy import create_engine
import os
import urllib


DB_CREDENTIALS = os.environ.get("DATABASE_PARAMS")
SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % urllib.parse.quote_plus(
    DB_CREDENTIALS
)

file = "lkp_postal_nodes.csv"
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)


def add_lrf_data():
    try:
        data = pd.read_csv(file, index_col=0)
        data.to_sql("lrf_data", engine, if_exists="replace")
    except Exception as e:
        print(e)
    else:
        pass


if __name__ == "__main__":
    add_lrf_data()
