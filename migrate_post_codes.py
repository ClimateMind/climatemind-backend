from sqlalchemy import create_engine
import os
import urllib
from app import db
from app.models import Scores, Sessions
import uuid
from app import create_app

app = create_app()
app.app_context().push()

# Create a connection to the database.

DB_CREDENTIALS = os.environ.get("DATABASE_PARAMS")
SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % urllib.parse.quote_plus(
    DB_CREDENTIALS
)

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

"""
This script was created and run on 29 August 2021 to migrate postal codes from the sessions table
to the scores table, as part of db refactoring.

"""


def migrate_data():
    with app.app_context():

        data_dict = dict()

        for row in Sessions.query.all():
            data_dict[row.session_uuid] = row.postal_code

        for row in Scores.query.all():
            if row.session_uuid in data_dict:
                row.postal_code = data_dict.get(row.session_uuid)

        db.session.commit()


if __name__ == "__main__":
    migrate_data()
