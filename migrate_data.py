from sqlalchemy import create_engine
import os
import urllib
from app import db
from app.models import Scores, Sessions, Signup, ClimateFeed
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
This script was created and run on 28 February 2021 to migrate existing data while refactoring 
the db structure to change the session_id primary and foreign keys from string format to UUID format 
(UNIQUEIDENTIFIER datatype in SQL Server). This script does NOT need to be re-run. It is maintained
here for documentation purposes only.

"""


def migrate_data():
    with app.app_context():
        for row in ClimateFeed.query.all():
            new_uuid = uuid.UUID(row.session_id)
            row.session_uuid = new_uuid

        for row in Scores.query.all():
            new_uuid = uuid.UUID(row.session_id)
            row.session_uuid = new_uuid

        for row in Signup.query.all():
            new_uuid = uuid.UUID(row.session_id)
            row.session_uuid = new_uuid

        for row in Sessions.query.all():
            new_uuid = uuid.UUID(row.session_id)
            row.session_uuid = new_uuid

        db.session.commit()


if __name__ == "__main__":
    migrate_data()
