import pytest
from flask import url_for
from freezegun import freeze_time
from mock import mock

from app.factories import faker, UsersFactory
from app.models import Sessions

faked_now = faker.date_time()


@freeze_time(faked_now)
@pytest.mark.integration
def test_post_session_creates_unique_uuids(client):
    user = UsersFactory()
    assert not Sessions.query.count(), "There should be no sessions"

    with mock.patch("flask_jwt_extended.utils.get_current_user", return_value=user):
        response = client.post(url_for("session.post_session"))
    assert response.status_code == 201, "Is success"
    assert Sessions.query.count() == 1, "Session should be created"

    session = Sessions.query.first()
    response_uuid = response.json.get("sessionId").upper()
    assert (
        session.session_uuid == response_uuid
    ), "The endpoint should return same UUID as stored in DB"
    assert (
        session.session_created_timestamp == faked_now
    ), "The session object has been created now"
    assert session.user_uuid == user.user_uuid, "Mocked user linked"
