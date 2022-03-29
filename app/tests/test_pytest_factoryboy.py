import pytest

from app.models import Users


def test_default_users_model_fixture_can_be_used(test_users, auth, db_session):
    assert db_session.query(Users).count() == 1
    assert Users.query.count() == 1

    db_user = Users.query.first()

    assert test_users.user_uuid == db_user.user_uuid
    assert test_users.check_password(pytest.config.get("TEST_PASSWORD"))


def test_users_model_is_function_scope_only(auth, db_session):
    assert db_session.query(Users).count() == 0
    assert Users.query.count() == 0


def test_users_factory_can_be_used(users_factory, auth, db_session):
    assert db_session.query(Users).count() == 0
    senior_pomidor = users_factory(first_name="Daniil", last_name="Mashkin")

    assert senior_pomidor.user_uuid == Users.query.first().user_uuid
    assert db_session.query(Users).count() == 1
    assert senior_pomidor.first_name == "Daniil"
    assert senior_pomidor.last_name == "Mashkin"

    second_pomidor = users_factory()
    assert db_session.query(Users).count() == 2
    assert senior_pomidor.user_uuid != second_pomidor.user_uuid


CUSTOM_PASS = "plant_based_password"


@pytest.mark.parametrize("users__password", [CUSTOM_PASS])
def test_users_password_generation_and_factoryboy_parametrize(users):
    assert users.check_password(CUSTOM_PASS)
