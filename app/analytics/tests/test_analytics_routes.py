from datetime import datetime, timedelta, timezone

import pytest
import typing
from flask import url_for
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token
from freezegun import freeze_time
from mock import mock

from app.factories import (
    UsersFactory,
    faker,
    SessionsFactory,
    PasswordResetLinkFactory,
    ScoresFactory,
)
from app.models import AnalyticsData, Users


@pytest.mark.integration
def test_add_event(client, accept_json):
    session = SessionsFactory()
    session_header = [("X-Session-Id", session.session_uuid)]
    ok_data = {
            "category": faker.pystr(20, 50),
            "action": faker.pystr(20, 50),
            "label": faker.pystr(20, 50),
            "eventValue": faker.pystr(20, 50),
            "eventTimestamp": str(faker.date_time()),
            "pageUrl": faker.pystr(20, 255),
    }

    url = url_for("analytics.post_user_a_event")
    response = client.post(
        url,
        headers=session_header,
        json=ok_data,
    )
    assert response.status_code == 201, "User event logged."



