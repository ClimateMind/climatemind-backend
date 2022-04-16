import pytest

from app.factories import UsersFactory
from app.models import Users


def test_factoryboy_can_be_used(auth, db_session):
    assert Users.query.count() == 0

    test_password = "reduce_dairy_and_meat_consumption_666"
    test_users = UsersFactory(password=test_password)
    assert db_session.query(Users).count() == 1
    assert Users.query.count() == 1

    db_user = Users.query.first()

    assert test_users.user_uuid == db_user.user_uuid
    assert test_users.check_password(test_password)


def test_factoryboy_is_funciton_scope_only(auth, db_session):
    assert db_session.query(Users).count() == 0
    assert Users.query.count() == 0
