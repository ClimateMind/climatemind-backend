import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError

from app import create_app
from app.extensions import db
from config import TestingConfig, DevelopmentConfig

app = create_app(TestingConfig)
app.app_context().push()


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
        with create_engine(
            DevelopmentConfig.SQLALCHEMY_DATABASE_URI,
            isolation_level="AUTOCOMMIT",
        ).connect() as connection:
            try:
                print(f"Trying to create {TestingConfig.DB_NAME} database...")
                connection.execute(f"CREATE DATABASE [{TestingConfig.DB_NAME}]")
                db.create_all()
                print(f"{TestingConfig.DB_NAME} created!")

            except ProgrammingError:
                print(f"Database {TestingConfig.DB_NAME} already exists.")
                reuse_db = session.config.getoption("--reuse-db")
                if not reuse_db:
                    print(f"Removing {TestingConfig.DB_NAME} database...")
                    connection.execute(f"DROP DATABASE [{TestingConfig.DB_NAME}]")
                    print(f"Trying to create new {TestingConfig.DB_NAME} database...")
                    connection.execute(f"CREATE DATABASE [{TestingConfig.DB_NAME}]")
                    db.create_all()
                    print(f"{TestingConfig.DB_NAME} created!")
                else:
                    print(f"Reusing existing database.")
