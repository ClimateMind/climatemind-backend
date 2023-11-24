import mock
import pytest
from mock.mock import Mock, MagicMock

from flask_jwt_extended import create_access_token
from flask import url_for

from app.factories import UsersFactory, SessionsFactory, faker
from app.models import Sessions
from app.session.session_helpers import store_session, get_ip_address

faked_session_uuid = faker.uuid4().upper()
faked_user_uuid = faker.uuid4().upper()
faked_datetime = faker.date_time()
faked_ip = faker.ipv4()


@pytest.mark.parametrize(
    "session_uuid, session_created_timestamp, user_uuid, ip_address",
    (
        (faked_session_uuid, faked_datetime, faked_user_uuid, faked_ip),
        (faked_session_uuid, faked_datetime, None, None),
    ),
)
def test_store_session_creation(
    session_uuid, session_created_timestamp, user_uuid, ip_address
):
    assert not Sessions.query.count(), "There should be no sessions"
    if user_uuid:
        UsersFactory(user_uuid=user_uuid)

    store_session(session_uuid, session_created_timestamp, user_uuid, ip_address)

    assert Sessions.query.count() == 1, "Single session should be created"
    created_session = Sessions.query.first()
    assert created_session.session_uuid == session_uuid
    db_time = created_session.session_created_timestamp.isoformat(" ", "seconds")
    expected_time = session_created_timestamp.isoformat(" ", "seconds")
    assert db_time == expected_time
    assert created_session.user_uuid == user_uuid
    assert created_session.ip_address == ip_address


@mock.patch("app.session.session_helpers.check_if_local", return_value=True)
def test_get_ip_address_local(mocked_check_if_local):
    assert get_ip_address(Mock()) is None, "Local IP should be None"
    mocked_check_if_local.assert_called_once()


@mock.patch("app.session.session_helpers.check_if_local", return_value=False)
def test_get_ip_address_prod(mocked_check_if_local):
    first_ip = faked_ip
    second_ip = faker.ipv4()
    request = MagicMock()
    request.headers.getlist.side_effect = [
        [],
        [first_ip],
        [first_ip, second_ip],
    ]

    assert get_ip_address(request) is None
    mocked_check_if_local.assert_called_once()
    request.headers.getlist.assert_called_once_with("X-Forwarded-For")

    assert get_ip_address(request) == first_ip
    assert get_ip_address(request) == first_ip


@pytest.mark.parametrize(
    "target,http_method",
    [
        ("myths.get_general_myths", "GET"),
        ("conversations.create_conversation_invite", "POST"),
        ("auth.login", "GET"),
        ("auth.logout", "POST"),
        ("auth.register", "POST"),
        ("alignment.post_alignment_uuid", "POST"),
        ("account.update_user_account", "PUT"),
        ("scoring.user_scores", "POST"),
    ],
)
def test_maybe_assign_session(target, http_method, client, accept_json):
    session = SessionsFactory(user=None)
    session_header = [("X-Session-Id", session.session_uuid)]

    client.open(
        url_for(target),
        method=http_method,
        headers=accept_json + session_header,
        json={},
    )

    assert (
        session.user_uuid is None
    ), "No user should be assigned to session yet (session={}, user={}).".format(
        session.session_uuid, session.user_uuid
    )

    user = UsersFactory()
    access_token = create_access_token(identity=user, fresh=True)
    auth_header = [("Authorization", "Bearer " + access_token)]

    client.open(
        url_for(target),
        method=http_method,
        headers=accept_json + session_header + auth_header,
        json={},
    )

    assert (
        session.user_uuid == user.user_uuid
    ), "Session user should now be set: ({},{}).".format(
        session.user_uuid, user.user_uuid
    )
