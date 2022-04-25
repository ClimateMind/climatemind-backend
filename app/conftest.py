import factory
import pytest
from flask_sqlalchemy import SQLAlchemy


@pytest.fixture(autouse=True)
def set_session_for_factories(db_session):
    session = db_session()
    for cls in factory.alchemy.SQLAlchemyModelFactory.__subclasses__():
        cls._meta.sqlalchemy_session = session

    yield


@pytest.fixture(scope="session")
def app(worker_id):
    yield pytest.config["APP"]


@pytest.fixture(scope="session")
def _db(app):
    """
    Provide the transactional fixtures with access to the database via
    a Flask-SQLAlchemy database connection.
    """
    db = SQLAlchemy(app=app)
    yield db
