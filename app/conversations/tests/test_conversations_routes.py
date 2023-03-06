import random
import typing
import uuid

import pytest
from flask import url_for
from flask.testing import FlaskClient
from mock import mock

from app.common.uuid import to_uuid
from app.common.tests.utils import assert_email_sent
from app.conversations.enums import (
    ConversationUserARating,
    ConversationState,
)
from app.user_b.analytics_logging import eventType
from app.factories import ConversationsFactory, faker, UserBJourneyFactory
from app.models import Conversations, Users, UserBAnalyticsData


@pytest.mark.integration
@pytest.mark.parametrize(
    "old_state,request_data,event_type,status_code",
    [
        (  # no fields
            None,
            {},
            None,
            200,
        ),
        (  # just receiver
            None,
            {
                "receiverName": faker.name(),
            },
            None,
            200,
        ),
        (  # cannot have state and rating together
            None,
            {
                "state": random.choice(list([s.value for s in ConversationState])),
                "userARating": random.choice(
                    list([s.value for s in ConversationUserARating])
                ),
            },
            None,
            422,
        ),
        (  # valid state transition
            ConversationState.TopicsButtonClicked,
            {"state": ConversationState.RatingDone},
            eventType.UA_RATING_DONE,
            200,
        ),
        (  # valid state transition
            ConversationState.AlignButtonClicked,
            {"state": ConversationState.TopicsButtonClicked},
            eventType.UA_TOPICS_CLICK,
            200,
        ),
        (  # valid state transition
            ConversationState.TopicsButtonClicked,
            {"state": ConversationState.TalkedButtonClicked},
            eventType.UA_TALKED_CLICK,
            200,
        ),
        (  # invalid state transition
            ConversationState.TalkedButtonClicked,
            {"state": ConversationState.TopicsButtonClicked},
            None,
            422,
        ),
        (  # invalid state transition
            ConversationState.RatingDone,
            {"state": ConversationState.TalkedButtonClicked},
            None,
            422,
        ),
        (  # cannot change from state to same state
            ConversationState.TopicsButtonClicked,
            {"state": ConversationState.TopicsButtonClicked},
            None,
            422,
        ),
        (  # receiver and valid state transition
            ConversationState.TopicsButtonClicked,
            {"receiverName": faker.name(), "state": ConversationState.RatingDone},
            eventType.UA_RATING_DONE,
            200,
        ),
    ],
)
def test_edit_conversation_request_data(
    old_state,
    request_data,
    event_type,
    status_code,
    client_with_user_and_header,
    accept_json,
):
    client, user, session_header, _ = client_with_user_and_header
    if old_state is None:
        conversation = ConversationsFactory(sender_user=user)
    else:
        conversation = ConversationsFactory(
            sender_user=user, state=ConversationState(old_state)
        )
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
        if event_type is None:
            assert UserBAnalyticsData.query.count() == 0, "No analytics event logged."
        else:
            assert (
                UserBAnalyticsData.query.count() == 1
            ), "An analytics event is logged."
            analytics_event = UserBAnalyticsData.query.first()
            assert (
                analytics_event.conversation_uuid == conversation.conversation_uuid
            ), "Analytics event has matching conversation id"
            assert (
                analytics_event.session_uuid == session_header[0][1]
            ), "Analytics event has matching session id"
            assert analytics_event.event_type == event_type.value
            assert analytics_event.event_value


def test_delete_conversation(client_with_user_and_header, accept_json):
    client, user, session_header, _ = client_with_user_and_header

    conversation = ConversationsFactory(sender_user=user)
    assert conversation.is_marked_deleted is False, "Conversation should be visible"
    assert Conversations.query.count() == 1, "Make sure we have a single Conversation"

    with mock.patch("flask_jwt_extended.utils.get_current_user", return_value=user):
        url = url_for(
            "conversations.delete_conversation",
            conversation_uuid=conversation.conversation_uuid,
        )

        response = client.delete(
            url,
            headers=session_header + accept_json,
        )

        assert response.status_code == 200, str(response.json)

    assert conversation.is_marked_deleted, "Conversation should not be visible"
    assert Conversations.query.count() == 1, "Conversations count kept the same."


def emulate_test_conversation_request_with_error(
    client: FlaskClient,
    user: Users,
    headers: list,
    test_uuid: typing.Union[uuid.UUID, str],
    endpoint_name: str,
):
    with mock.patch("flask_jwt_extended.utils.get_current_user", return_value=user):
        url = url_for(
            endpoint_name,
            conversation_uuid=test_uuid,
        )
        response = client.put(
            url,
            json={"receiver_name": "unbeliever"},
            headers=headers,
        )
        return response


@pytest.mark.integration
def test_conversation_request_without_session(client_with_user_and_header, accept_json):
    client, user, _, _ = client_with_user_and_header
    conversation = ConversationsFactory(sender_user=user)

    endpoints_to_test = [
        "conversations.edit_conversation",
        "conversations.delete_conversation",
    ]
    for endpoint_name in endpoints_to_test:
        response = emulate_test_conversation_request_with_error(
            client, user, accept_json, conversation.conversation_uuid, endpoint_name
        )

        assert response.status_code == 400, "Missing session header"


@pytest.mark.integration
def test_conversation_request_invalid_uuid(client_with_user_and_header, accept_json):
    client, user, session_header, _ = client_with_user_and_header

    headers = session_header + accept_json
    endpoints_to_test = [
        "conversations.edit_conversation",
        "conversations.delete_conversation",
    ]
    for endpoint in endpoints_to_test:
        response = emulate_test_conversation_request_with_error(
            client, user, headers, "invalid uuid", endpoint
        )

        assert response.status_code == 400, "Invalid convo UUID provided"


@pytest.mark.integration
def test_conversation_request_not_found(client_with_user_and_header, accept_json):
    client, user, session_header, _ = client_with_user_and_header
    conversation = ConversationsFactory(sender_user=user)
    wrong_convo_uuid = faker.uuid4()
    assert conversation.conversation_uuid != wrong_convo_uuid

    headers = session_header + accept_json
    endpoints_to_test = [
        "conversations.edit_conversation",
        "conversations.delete_conversation",
    ]
    for endpoint in endpoints_to_test:
        response = emulate_test_conversation_request_with_error(
            client, user, headers, wrong_convo_uuid, endpoint
        )

        assert response.status_code == 404, "Convo with this UUID should not be found"


@pytest.mark.integration
def test_conversation_request_forbidden(client_with_user_and_header, accept_json):
    client, user, session_header, _ = client_with_user_and_header
    conversation = ConversationsFactory()
    assert user.user_uuid != conversation.sender_user_uuid, "Users should be different"

    headers = session_header + accept_json
    endpoints_to_test = [
        "conversations.edit_conversation",
        "conversations.delete_conversation",
    ]
    for endpoint in endpoints_to_test:
        response = emulate_test_conversation_request_with_error(
            client, user, headers, conversation.conversation_uuid, endpoint
        )

        assert response.status_code == 403, "Convo sender_user mismatch"


@pytest.mark.integration
def test_conversation_request_unauthorized(client_with_user_and_header, accept_json):
    client, user, session_header, _ = client_with_user_and_header
    client.delete_cookie("localhost", "access_token")

    conversation = ConversationsFactory(sender_user=user)

    headers = session_header + accept_json
    endpoints_to_test = [
        "conversations.edit_conversation",
        "conversations.delete_conversation",
    ]
    for endpoint in endpoints_to_test:
        response = emulate_test_conversation_request_with_error(
            client, user, headers, conversation.conversation_uuid, endpoint
        )

        assert response.status_code == 401, "Unauthorized access forbidden"


@pytest.mark.integration
def test_consent_sends_user_b_shared_email(sendgrid_mock, client_with_user_and_header):
    user_b_journey = UserBJourneyFactory()
    conversation_uuid = user_b_journey.conversation.conversation_uuid
    url = url_for("conversations.post_consent", conversation_uuid=conversation_uuid)

    client, _, session_header, _ = client_with_user_and_header
    client.post(url, headers=session_header, json={"consent": True})

    assert_email_sent(
        sendgrid_mock,
        subject_starts_with="Ready for a climate conversation",
        base_frontend_url="http://localhost:3000",
    )


@pytest.mark.integration
@mock.patch("app.sendgrid.utils.current_app")
def test_consent_sends_user_b_shared_email_with_configured_base_frontend_url(
    m_current_app, sendgrid_mock, client_with_user_and_header
):
    m_current_app.config.get.side_effect = (
        lambda key: "https://fake-url.local" if key == "BASE_FRONTEND_URL" else None
    )

    user_b_journey = UserBJourneyFactory()
    conversation_uuid = user_b_journey.conversation.conversation_uuid
    url = url_for("conversations.post_consent", conversation_uuid=conversation_uuid)

    client, _, session_header, _ = client_with_user_and_header
    client.post(url, headers=session_header, json={"consent": True})

    assert_email_sent(
        sendgrid_mock,
        subject_starts_with="Ready for a climate conversation",
        base_frontend_url="https://fake-url.local",
    )


def test_get_conversations_empty(client_with_user_and_header, accept_json):
    client, _, session_header, _ = client_with_user_and_header
    url = url_for("conversations.get_conversations")
    response = client.get(
        url,
        headers=session_header + accept_json,
    )
    assert response.status_code == 200, str(response.json)
    assert response.json == {"conversations": []}


@pytest.mark.parametrize(
    "invited_user_name",
    [
        "",
        "managementmanagementm",
        "managementmanagementmanagementmanagementmanagementm",
    ],
)
@pytest.mark.integration
def test_create_conversation_with_invalid_invitee(
    invited_user_name, client_with_user_and_header, accept_json
):
    client, _, session_header, _ = client_with_user_and_header
    url = url_for("conversations.create_conversation_invite")
    response = client.post(
        url,
        headers=session_header + accept_json,
        json={"invitedUserName": invited_user_name},
    )
    assert (
        response.status_code == 400
    ), "Must provide a JSON body with the name of the invited user."


@pytest.mark.integration
def test_create_conversation_with_invalid_body(
    client_with_user_and_header, accept_json
):
    client, _, session_header, _ = client_with_user_and_header
    url = url_for("conversations.create_conversation_invite")
    response = client.post(
        url,
        headers=session_header + accept_json,
        json=faker.name(),
    )
    assert (
        response.status_code == 400
    ), "Must provide a JSON body with the name of the invited user."


@pytest.mark.integration
def test_create_conversation_with_invalid_session(
    client_with_user_and_header, accept_json
):
    client, _, session_header, _ = client_with_user_and_header
    url = url_for("conversations.create_conversation_invite")
    bad_session_header = [("X-Session-Id", faker.uuid4().upper())]
    assert bad_session_header != session_header
    response = client.post(
        url,
        headers=bad_session_header + accept_json,
        json={"invitedUserName": faker.name()},
    )
    assert response.status_code == 404, "SESSION_UUID is not in the db."


@pytest.mark.integration
def test_create_conversation_successful(client_with_user_and_header, accept_json):
    client, _, session_header, _ = client_with_user_and_header
    url = url_for("conversations.create_conversation_invite")
    response = client.post(
        url,
        headers=session_header + accept_json,
        json={"invitedUserName": faker.name()},
    )
    assert response.status_code == 201, str(response.json)
    assert (
        response.json["message"] == "conversation created"
    ), 'Successful creation should give "conversation created" message.'
    assert (
        response.json["conversationId"] == response.json["conversationId"].lower()
    ), "conversationId uuid should be lower case."
    assert to_uuid(
        response.json["conversationId"]
    ), "conversationId is not a valid uuid."


@pytest.mark.integration
def test_create_conversations_successful(client_with_user_and_header, accept_json):
    client, _, session_header, _ = client_with_user_and_header
    url_create = url_for("conversations.create_conversation_invite")
    for i in range(3):
        client.post(
            url_create,
            headers=session_header + accept_json,
            json={"invitedUserName": faker.name()},
        )
    url_list = url_for("conversations.get_conversations")
    response = client.get(url_list, headers=session_header + accept_json)
    assert isinstance(response.json["conversations"], list), response.json

    for conversation in response.json["conversations"]:

        assert (
            "conversationId" in conversation.keys()
        ), "Conversation must include conversationId."
        assert (
            conversation["conversationId"] == conversation["conversationId"].upper()
        ), "conversationId uuid must be upper case."
        assert to_uuid(
            conversation["conversationId"]
        ), "conversationId must be a valid uuid."

        assert "state" in conversation.keys(), "Conversation must include state."
        assert isinstance(conversation["state"], int), "state must be an int."

        assert "userA" in conversation.keys(), "Conversation must include userA."
        assert isinstance(conversation["userA"], dict), "userA must be a dict."

        assert (
            "sessionId" in conversation["userA"].keys()
        ), "userA must include sessionId."
        assert (
            conversation["userA"]["sessionId"]
            == conversation["userA"]["sessionId"].upper()
        ), "userA sessionId uuid must be upper case."
        assert to_uuid(
            conversation["userA"]["sessionId"]
        ), "userA sessionId uuid must be a valid uuid."

        assert "id" in conversation["userA"].keys(), "userA must include id."
        assert (
            conversation["userA"]["id"] == conversation["userA"]["id"].upper()
        ), "userA id uuid must be upper case."
        assert to_uuid(
            conversation["userA"]["id"]
        ), "userA id uuid must be a valid uuid."

        assert "name" in conversation["userA"].keys(), "userA must include name."
        assert isinstance(
            conversation["userA"]["name"], str
        ), "userA name must be a str."

        assert "userB" in conversation.keys(), "Conversation must include userB."
        assert isinstance(conversation["userB"], dict), "userB must be a dict."

        assert "name" in conversation["userB"].keys(), "userB must include name."
        assert isinstance(
            conversation["userB"]["name"], str
        ), "userB name must be a str."

        assert (
            "userARating" in conversation.keys()
        ), "Conversation must include userARating."
        assert "consent" in conversation.keys(), "Conversation must include consent."
        assert (
            "conversationTimestamp" in conversation.keys()
        ), "Conversation must include conversationTimestamp."
        assert (
            "alignmentScoresId" in conversation.keys()
        ), "Conversation must include alignmentScoresId."
