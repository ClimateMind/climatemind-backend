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


def pytest_sessionstart(session):
    workerinput = getattr(session.config, "workerinput", None)
    if workerinput is None:
        print(f"Creating new {TestingConfig.DB_NAME} database...")
        with create_engine(
            DevelopmentConfig.SQLALCHEMY_DATABASE_URI,
            isolation_level="AUTOCOMMIT",
        ).connect() as connection:

            try:
                connection.execute(f"CREATE DATABASE [{TestingConfig.DB_NAME}]")
            except ProgrammingError:
                connection.execute(f"DROP DATABASE [{TestingConfig.DB_NAME}]")
                connection.execute(f"CREATE DATABASE [{TestingConfig.DB_NAME}]")

            db.create_all()
        print(f"{TestingConfig.DB_NAME} created!")


def pytest_sessionfinish(session):
    workerinput = getattr(session.config, "workerinput", None)
    if workerinput is None:
        print(f"\nCleanup {TestingConfig.DB_NAME} database...")
        with create_engine(
            DevelopmentConfig.SQLALCHEMY_DATABASE_URI,
            isolation_level="AUTOCOMMIT",
        ).connect() as connection:
            connection.execute(f"DROP DATABASE [{TestingConfig.DB_NAME}]")
        print(f"DB {TestingConfig.DB_NAME} removed!")
