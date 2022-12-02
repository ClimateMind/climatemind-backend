import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError

from app import create_app
from app.extensions import db
from config import TestingConfig, DevelopmentConfig
from migrations.scripts.lrf.add_lrf_table import add_lrf_data

from flask import request
from app.session.session_helpers import maybe_assign_session


app = create_app(TestingConfig)
app.app_context().push()


@app.before_request
def before_request_hook():
    maybe_assign_session(request)


def pytest_configure():
    """Make the following constants available across all pytest unit tests."""
    pytest.config = {
        "APP": app,
    }


def pytest_addoption(parser):
    parser.addoption(
        "--reuse-db",
        action="store_true",
        help="Use this argument to reuse existing db.",
    )


def pytest_sessionstart(session):
    workerinput = getattr(session.config, "workerinput", None)
    if workerinput is None:
        engine = create_engine(
            DevelopmentConfig.SQLALCHEMY_DATABASE_URI,
            isolation_level="AUTOCOMMIT",
            fast_executemany=True,
        )

        with engine.connect() as connection:
            try:
                create_new_test_database(engine, connection)

            except ProgrammingError:
                print(f"Database {TestingConfig.DB_NAME} already exists.")
                reuse_db = session.config.getoption("--reuse-db")
                if not reuse_db:
                    print(f"Removing {TestingConfig.DB_NAME} database...")
                    connection.execute(f"DROP DATABASE [{TestingConfig.DB_NAME}]")
                    create_new_test_database(engine, connection)
                else:
                    print("Reusing existing database.")


def create_new_test_database(engine, connection):
    print(f"Trying to create new {TestingConfig.DB_NAME} database...")
    connection.execute(f"CREATE DATABASE [{TestingConfig.DB_NAME}]")
    db.create_all()
    add_lrf_data(engine)
    print(f"{TestingConfig.DB_NAME} created!")
