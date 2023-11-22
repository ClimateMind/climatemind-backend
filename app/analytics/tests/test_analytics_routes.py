from datetime import datetime, timedelta

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
)
from app.models import AnalyticsData, Users


@pytest.mark.integration
def test_add_event(client_with_user_and_header):
    client, user, session_header, current_password = client_with_user_and_header

    url = url_for("analytics.post_user_a_event")
    headers = session_header + accept_json
    response = client.post(
        url,
        headers=headers,
        json={
            "category": faker.pystr(20, 50),
            "action": faker.pystr(20, 50),
            "label": faker.pystr(20, 50),
            "eventValue": faker.pystr(20, 50),
            "eventTimestamp": faker.date_time(),
            "pageUrl": faker.pystr(20, 255),
        },
    )

assert response.status_code == 201, "User event logged."



