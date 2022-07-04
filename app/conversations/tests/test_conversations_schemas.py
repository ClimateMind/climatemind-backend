import typing
import uuid

import pytest
from marshmallow import ValidationError

from app.conversations.enums import (
    ConversationState,
    ConversationUserARating,
)
from app.conversations.schemas import ConversationEditSchema
from app.factories import ConversationsFactory, faker


def test_conversation_edit_schema_state_could_only_increase():
    conversation = ConversationsFactory(state=ConversationState.UserBInvited)
    schema = ConversationEditSchema()

    ordered_states = list(ConversationState)[1:]

    for state in ordered_states:
        data = get_conversation_edit_schema_data_to_load(
            conversation.conversation_uuid, state
        )

        if data:
            conversation = schema.load(data, instance=conversation, partial=True)
            assert conversation.state == state

    reverse_ordered_states = sorted(list(ConversationState), reverse=True)
    for state in reverse_ordered_states:
        data = get_conversation_edit_schema_data_to_load(
            conversation.conversation_uuid, state
        )
        if data:
            if not data.get("userARating"):
                with pytest.raises(ValidationError):
                    conversation = schema.load(data, partial=True)
            else:
                conversation = schema.load(data, partial=True)
                assert True, "It's fine to update edit rating"


def get_conversation_edit_schema_data_to_load(
    conversation_uuid: uuid.UUID, state: ConversationState
) -> typing.Optional[dict]:
    data = {"conversationId": conversation_uuid}

    if state == ConversationState.RatingDone:
        data["userARating"] = ConversationUserARating.EXCELLENT
    else:
        data["state"] = state

    return data


@pytest.mark.parametrize(
    "field_name,good_values,bad_values",
    (
        ("userARating", list(ConversationUserARating), [999, "123"]),
        (
            "state",
            list(ConversationState),
            ["123", "align", 999],
        ),
        ("receiverName", [faker.name(), "Test", "123"], [1]),
    ),
)
def test_conversation_edit_schema_base_validation(
    field_name: str, good_values: list, bad_values: list
):
    schema = ConversationEditSchema()

    for good_value in good_values:
        data = {field_name: good_value}
        try:
            schema.load(data, partial=True)
            assert True, "All good"
        except ValidationError as e:
            assert False, f"{e.messages} raised but should not be"

    for bad_value in bad_values:
        with pytest.raises(ValidationError):
            data = {field_name: bad_value}
            schema.load(data, partial=True)
