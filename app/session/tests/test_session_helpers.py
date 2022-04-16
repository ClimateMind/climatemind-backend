import pytest
from faker import Factory

from app.factories import UsersFactory
from app.models import Sessions
from app.session.session_helpers import store_session

faker = Factory.create()

faked_session_uuid = faker.uuid4().upper()
faked_user_uuid = faker.uuid4().upper()
faked_datetime = faker.date_time()


@pytest.mark.parametrize(
    "session_uuid, session_created_timestamp, user_uuid",
    (
        (faked_session_uuid, faked_datetime, faked_user_uuid),
        (faked_session_uuid, faked_datetime, None),
    ),
)
def test_store_session_creation(session_uuid, session_created_timestamp, user_uuid):
    assert not Sessions.query.count(), "There should be no sessions"
    if user_uuid:
        UsersFactory(user_uuid=user_uuid)

    store_session(session_uuid, session_created_timestamp, user_uuid)

    assert Sessions.query.count() == 1, "Single session should be created"
    created_session = Sessions.query.first()
    assert created_session.session_uuid == session_uuid.upper()
    assert created_session.session_created_timestamp == session_created_timestamp
    assert created_session.user_uuid == user_uuid
