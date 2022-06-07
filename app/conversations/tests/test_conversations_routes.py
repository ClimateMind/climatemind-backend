import random
import typing
import uuid

import pytest
from flask import url_for
from flask.testing import FlaskClient
from mock import mock

from app.conversations.enums import ConversationStatus
from app.factories import ConversationsFactory, faker
from app.models import Conversations, Users

RANDOM_CONVERSATION_STATUS = random.choice(list([s.value for s in ConversationStatus]))


@pytest.mark.integration
@pytest.mark.parametrize(
    "request_data,status_code",
    [
        ({"receiverName": faker.name()}, 200),
        ({"conversationStatus": RANDOM_CONVERSATION_STATUS}, 200),
        ({"conversationStatus": 999}, 422),  # beyond enum
        ({"conversationStatus": "wrong type"}, 422),  # type error
        (
            {
                "receiverName": faker.name(),
                "conversationStatus": RANDOM_CONVERSATION_STATUS,
            },
            200,
        ),
        ({"receiver_name": faker.name()}, 422),  # name error
        ({"userBShareConsent": faker.pybool()}, 422),  # user A cannot change consent
    ],
)
def test_edit_conversation_request_data(
    request_data, status_code, client_with_user_and_header, accept_json
):
    client, user, session_header, _ = client_with_user_and_header

    expected_response_keys = {
        "conversationId",
        "conversationStatus",
        "receiverName",
    }

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

        response_json_keys = response.json.keys()
        if response.status_code == 200:
            assert set(response_json_keys) == expected_response_keys
            for request_key, request_value in request_data.items():
                assert response.json[request_key] == request_value, "All values updated"
        else:
            expected_keys_while_error = ["error"]
            assert (
                list(response_json_keys) == expected_keys_while_error
            ), "Should return a validation errors"

            actual_errors_in_parent_object = set(response.json["error"].keys())
            expected_errors_in_parent_object = set(request_data.keys())
            assert (
                actual_errors_in_parent_object == expected_errors_in_parent_object
            ), "Errors only"

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
