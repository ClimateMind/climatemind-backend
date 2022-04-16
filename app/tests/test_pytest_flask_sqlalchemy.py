from app.factories import UsersFactory
from app.models import Users


def test_that_session_is_mocked(db_session):
    from app.extensions import db

    assert db.session is db_session
    assert Users.query.session is db_session()
    assert UsersFactory._meta.sqlalchemy_session is db_session()
