import random
import typing
import uuid

import pytest
from flask import url_for
from flask.testing import FlaskClient
from mock import mock

from app.conversations.enums import (
    ConversationUserARating,
    ConversationState,
)
from app.factories import ConversationsFactory, faker
from app.models import Conversations, Users

RANDOM_CONVERSATION_STATE = random.choice(list([s.value for s in ConversationState]))


@pytest.mark.skip("FIXME")
@pytest.mark.integration
@pytest.mark.parametrize(
    "request_data,status_code",
    [
        (
            {
                "receiverName": faker.name(),
                "state": RANDOM_CONVERSATION_STATE,
            },
            200,
        ),
        (  # unable to use together
            {
                "userARating": ConversationUserARating.EXCELLENT,
                "state": RANDOM_CONVERSATION_STATE,
            },
            422,
        ),
    ],
)
def test_edit_conversation_request_data(
    request_data, status_code, client_with_user_and_header, accept_json
):
    client, user, session_header, _ = client_with_user_and_header

    conversation = ConversationsFactory(sender_user=user)
    assert Conversations.query.count() == 1, "Make sure we have a single Conversation"

    with mock.patch("flask_jwt_extended.utils.get_current_user", return_value=user):
        url = url_for(
            "conversations.edit_conversation",
            conversation_uuid=conversation.conversation_uuid,
        )

        response = client.put(
            url,
            headers=session_header + accept_json,
            json=request_data,
        )

        assert response.status_code == status_code, str(response.json)

    assert Conversations.query.count() == 1, "Conversations count kept the same."


def emulate_test_edit_conversation_request_with_error(
    client: FlaskClient,
    user: Users,
    headers: list,
    test_uuid: typing.Union[uuid.UUID, str],
):
    with mock.patch("flask_jwt_extended.utils.get_current_user", return_value=user):
        url = url_for(
            "conversations.edit_conversation",
            conversation_uuid=test_uuid,
        )
        response = client.put(
            url,
            json={"receiver_name": "unbeliever"},
            headers=headers,
        )
        return response


@pytest.mark.integration
def test_edit_conversation_request_without_session(
    client_with_user_and_header, accept_json
):
    client, user, _, _ = client_with_user_and_header
    conversation = ConversationsFactory(sender_user=user)

    response = emulate_test_edit_conversation_request_with_error(
        client, user, accept_json, conversation.conversation_uuid
    )

    assert response.status_code == 400, "Missing session header"


@pytest.mark.integration
def test_edit_conversation_request_invalid_uuid(
    client_with_user_and_header, accept_json
):
    client, user, session_header, _ = client_with_user_and_header

    headers = session_header + accept_json
    response = emulate_test_edit_conversation_request_with_error(
        client, user, headers, "invalid uuid"
    )

    assert response.status_code == 400, "Invalid convo UUID provided"


@pytest.mark.integration
def test_edit_conversation_request_not_found(client_with_user_and_header, accept_json):
    client, user, session_header, _ = client_with_user_and_header
    conversation = ConversationsFactory(sender_user=user)
    wrong_convo_uuid = faker.uuid4()
    assert conversation.conversation_uuid != wrong_convo_uuid

    headers = session_header + accept_json
    response = emulate_test_edit_conversation_request_with_error(
        client, user, headers, wrong_convo_uuid
    )

    assert response.status_code == 404, "Convo with this UUID should not be found"


@pytest.mark.integration
def test_edit_conversation_request_forbidden(client_with_user_and_header, accept_json):
    client, user, session_header, _ = client_with_user_and_header
    conversation = ConversationsFactory()
    assert user.user_uuid != conversation.sender_user_uuid, "Users should be different"

    headers = session_header + accept_json
    response = emulate_test_edit_conversation_request_with_error(
        client, user, headers, conversation.conversation_uuid
    )

    assert response.status_code == 403, "Convo sender_user mismatch"


@pytest.mark.integration
def test_edit_conversation_request_unauthorized(
    client_with_user_and_header, accept_json
):
    client, user, session_header, _ = client_with_user_and_header
    client.delete_cookie("localhost", "access_token")

    conversation = ConversationsFactory(sender_user=user)

    headers = session_header + accept_json
    response = emulate_test_edit_conversation_request_with_error(
        client, user, headers, conversation.conversation_uuid
    )

    assert response.status_code == 401, "Unauthorized access forbidden"
