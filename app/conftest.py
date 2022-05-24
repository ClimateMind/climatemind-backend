import typing

import factory
import pytest
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token
from flask_sqlalchemy import SQLAlchemy

from app.models import Users


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


@pytest.fixture()
def client_with_user_and_header(
    client: FlaskClient,
) -> typing.Tuple[FlaskClient, Users, list]:
    from app.factories import UsersFactory, SessionsFactory

    user = UsersFactory()
    session = SessionsFactory(user=user)
    access_token = create_access_token(identity=user, fresh=True)
    client.set_cookie("localhost", "access_token", access_token)

    session_header = [("X-Session-Id", session.session_uuid)]
    return client, user, session_header
