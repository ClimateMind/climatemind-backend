import pandas as pd
from sqlalchemy import create_engine
import os
import urllib

# Create a connection to the database.

DB_CREDENTIALS = os.environ.get("DATABASE_PARAMS")
SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % urllib.parse.quote_plus(
    DB_CREDENTIALS
)

# Change file variable when an updated CSV needs to be used.

file = "lkp_postal_nodes.csv"
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

# Create a new table (with data) based on the CSV file whenever the docker container is rebuilt.
def add_lrf_data():
    """
    Input:
        file = lkp_postal_nodes csv file

    Output:
        SQL statement POST-ed to database through SQLAlchemy
    """
    try:
        data = pd.read_csv(file=file, index_col=0)
        data.to_sql("lrf_data", engine, if_exists="replace")
    except Exception as e:
        print(e)
    else:
        pass


if __name__ == "__main__":
    add_lrf_data()
