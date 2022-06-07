import uuid

import pytest

from app.common.uuid import validate_uuid, uuidType, check_uuid_in_db
from app.errors.errors import InvalidUsageError, NotInDatabaseError
from app.factories import (
    faker,
    ScoresFactory,
    SessionsFactory,
    UsersFactory,
    ConversationsFactory,
    AlignmentScoresFactory,
    PasswordResetLinkFactory,
)

faked_uuid = faker.uuid4()


@pytest.mark.parametrize(
    "uuid_to_validate, exception",
    (
        (None, InvalidUsageError),
        ("invalid_uuid", InvalidUsageError),
        (1, InvalidUsageError),
        (faked_uuid, None),
    ),
)
def test_validate_uuid(uuid_to_validate, exception):
    current_type = uuidType.ALIGNMENT_SCORES
    if not exception:
        validated_uuid = validate_uuid(uuid_to_validate, current_type)
        assert str(validated_uuid) == uuid_to_validate
    else:
        with pytest.raises(exception):
            validate_uuid(uuid_to_validate, current_type)


@pytest.mark.parametrize(
    "uuid_type, factory_cls, uuid_field_name",
    (
        (uuidType.SESSION, SessionsFactory, "session_uuid"),
        (uuidType.QUIZ, ScoresFactory, "quiz_uuid"),
        (uuidType.USER, UsersFactory, "user_uuid"),
        (
            uuidType.CONVERSATION,
            ConversationsFactory,
            "conversation_uuid",
        ),
        (
            uuidType.ALIGNMENT_SCORES,
            AlignmentScoresFactory,
            "alignment_scores_uuid",
        ),
        (
            uuidType.RESET_PASSWORD_LINK,
            PasswordResetLinkFactory,
            "uuid",
        ),
    ),
)
def test_check_uuid_in_db(uuid_type, factory_cls, uuid_field_name):
    kwargs = {uuid_field_name: faked_uuid.upper()}
    obj = factory_cls(**kwargs)
    assert obj == check_uuid_in_db(faked_uuid, uuid_type)


def test_check_uuid_not_found_in_db():
    for uuid_type in uuidType:
        with pytest.raises(NotInDatabaseError):
            check_uuid_in_db(faked_uuid, uuid_type)
