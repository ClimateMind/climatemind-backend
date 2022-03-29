import factory
import pytest
from flask_sqlalchemy import SQLAlchemy
from pytest_factoryboy import register
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError

from app import create_app
from app.extensions import db
from app.factories import UsersFactory
from config import DevelopmentConfig, TestingConfig

TEST_PASSWORD = "reduce_dairy_and_meat_consumption_666"
register(UsersFactory, "test_users", password=TEST_PASSWORD)


for cls in factory.alchemy.SQLAlchemyModelFactory.__subclasses__():
    register(cls)


def pytest_configure():
    """Make the following constants available across all pytest unit tests."""
    pytest.config = {
        "TEST_PASSWORD": TEST_PASSWORD,
    }


@pytest.fixture(autouse=True)
def set_session_for_factories(db_session):
    session = db_session()
    for cls in factory.alchemy.SQLAlchemyModelFactory.__subclasses__():
        cls._meta.sqlalchemy_session = session

    yield


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username, password):
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)


@pytest.fixture(scope="session")
def database_instance():
    with create_engine(
        DevelopmentConfig.SQLALCHEMY_DATABASE_URI,
        isolation_level="AUTOCOMMIT",
        echo=True,
    ).connect() as connection:
        try:
            connection.execute(f"CREATE DATABASE [{TestingConfig.DB_NAME}]")
        except ProgrammingError:
            connection.execute(f"DROP DATABASE [{TestingConfig.DB_NAME}]")
            connection.execute(f"CREATE DATABASE [{TestingConfig.DB_NAME}]")

        yield
        connection.execute(f"DROP DATABASE [{TestingConfig.DB_NAME}]")


@pytest.fixture(scope="session")
def app(database_instance):
    app = create_app(config_class=TestingConfig)
    with app.app_context():
        db.create_all()
        yield app


@pytest.fixture(scope="session")
def _db(app):
    """
    Provide the transactional fixtures with access to the database via
    a Flask-SQLAlchemy database connection.
    """
    db = SQLAlchemy(app=app)
    yield db
