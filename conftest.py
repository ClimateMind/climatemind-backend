import pytest
from sqlalchemy.exc import ProgrammingError

from app import create_app
from app.common.db_utils import create_sqlalchemy_engine
from app.extensions import db
from config import TestingConfig
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
    should_add_lrf_data = session_config_has_lrf_data_enabled(session.config)
    if workerinput is None:
        engine = create_sqlalchemy_engine(
            isolation_level="AUTOCOMMIT",
            fast_executemany=True,
        )

        with engine.connect() as connection:
            try:
                create_new_test_database(engine, connection, should_add_lrf_data)

            except ProgrammingError:
                print(f"Database {TestingConfig.DB_NAME} already exists.")
                reuse_db = session.config.getoption("--reuse-db")
                if not reuse_db:
                    print(f"Removing {TestingConfig.DB_NAME} database...")
                    connection.execute(f"DROP DATABASE [{TestingConfig.DB_NAME}]")
                    create_new_test_database(engine, connection, should_add_lrf_data)
                else:
                    print("Reusing existing database.")


def session_config_has_lrf_data_enabled(session_config):
    marker_option = session_config.getoption("-m")
    print("marker_option", marker_option)
    return (
        "lrf_data or not lrf_data" in marker_option
        or "not lrf_data or lrf_data" in marker_option
        or ("not lrf_data" not in marker_option and "lrf_data" in marker_option)
    )


def create_new_test_database(engine, connection, should_add_lrf_data):
    print(f"Trying to create new {TestingConfig.DB_NAME} database...")
    connection.execute(f"CREATE DATABASE [{TestingConfig.DB_NAME}]")
    db.create_all()
    if should_add_lrf_data:
        add_lrf_data(engine)
    print(f"{TestingConfig.DB_NAME} created!")
