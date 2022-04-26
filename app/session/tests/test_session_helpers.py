import mock
import pytest
from mock.mock import Mock, MagicMock

from app.factories import UsersFactory, faker
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
    assert created_session.session_created_timestamp == session_created_timestamp
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
