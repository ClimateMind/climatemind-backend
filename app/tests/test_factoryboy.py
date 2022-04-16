import pytest

from app.factories import UsersFactory
from app.models import Users


def test_factoryboy_can_be_used(auth, db_session):
    assert Users.query.count() == 0

    test_users = UsersFactory(password=pytest.config.get("TEST_PASSWORD"))
    assert db_session.query(Users).count() == 1
    assert Users.query.count() == 1

    db_user = Users.query.first()

    assert test_users.user_uuid == db_user.user_uuid
    assert test_users.check_password(pytest.config.get("TEST_PASSWORD"))


def test_factoryboy_is_funciton_scope_only(auth, db_session):
    assert db_session.query(Users).count() == 0
    assert Users.query.count() == 0
