import random
import typing

import factory
from faker import Factory as FakerFactory
from werkzeug.security import generate_password_hash

from app.conversations.routes import ConversationStatus
from app.models import (
    Users,
    Sessions,
    Scores,
    Conversations,
    AlignmentScores,
    UserBJourney,
    AlignmentFeed,
    EffectChoice,
    SolutionChoice,
)
from app.personal_values.enums import PersonalValue
from app.scoring.process_alignment_scores import get_max, as_percent

faker = FakerFactory.create()


class UsersFactory(factory.alchemy.SQLAlchemyModelFactory):
    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_name = factory.LazyAttribute(lambda x: faker.last_name())
    user_uuid = factory.Sequence(lambda x: faker.uuid4().upper())
    user_email = factory.Sequence(lambda x: faker.email())
    password = factory.LazyAttribute(lambda x: faker.password())
    password_hash = factory.LazyAttribute(lambda o: generate_password_hash(o.password))

    class Meta:
        model = Users
        exclude = ("password",)


class SessionsFactory(factory.alchemy.SQLAlchemyModelFactory):
    ip_address = factory.LazyAttribute(lambda x: faker.ipv4())
    user = factory.SubFactory(UsersFactory)
    session_uuid = factory.Sequence(lambda x: faker.uuid4().upper())
    session_created_timestamp = factory.LazyAttribute(lambda x: faker.date_time())

    class Meta:
        model = Sessions


class ScoresFactory(factory.alchemy.SQLAlchemyModelFactory):
    quiz_uuid = factory.Sequence(lambda x: faker.uuid4().upper())
    scores_created_timestamp = factory.LazyAttribute(lambda x: faker.date_time())
    session = factory.SubFactory(SessionsFactory)
    postal_code = factory.LazyAttribute(lambda x: faker.postcode())

    security = factory.LazyAttribute(lambda x: faker.pyfloat(0, 1, True))
    conformity = factory.LazyAttribute(lambda x: faker.pyfloat(0, 1, True))
    benevolence = factory.LazyAttribute(lambda x: faker.pyfloat(0, 1, True))
    tradition = factory.LazyAttribute(lambda x: faker.pyfloat(0, 1, True))
    universalism = factory.LazyAttribute(lambda x: faker.pyfloat(0, 1, True))
    self_direction = factory.LazyAttribute(lambda x: faker.pyfloat(0, 1, True))
    stimulation = factory.LazyAttribute(lambda x: faker.pyfloat(0, 1, True))
    hedonism = factory.LazyAttribute(lambda x: faker.pyfloat(0, 1, True))
    achievement = factory.LazyAttribute(lambda x: faker.pyfloat(0, 1, True))
    power = factory.LazyAttribute(lambda x: faker.pyfloat(0, 1, True))

    class Meta:
        model = Scores


class ConversationsFactory(factory.alchemy.SQLAlchemyModelFactory):
    conversation_uuid = factory.Sequence(lambda x: faker.uuid4().upper())
    sender_user = factory.SubFactory(UsersFactory)
    sender_session = factory.SubFactory(SessionsFactory)
    receiver_name = factory.LazyAttribute(lambda x: faker.name())
    conversation_status = factory.LazyAttribute(
        lambda x: faker.pyint(min(ConversationStatus), max(ConversationStatus))
    )
    conversation_created_timestamp = factory.LazyAttribute(lambda x: faker.date_time())
    user_b_share_consent = factory.LazyAttribute(lambda x: faker.pybool())

    class Meta:
        model = Conversations


class AlignmentScoresFactory(factory.alchemy.SQLAlchemyModelFactory):
    alignment_scores_uuid = factory.Sequence(lambda x: faker.uuid4().upper())
    # FIXME: should be based on conversation
    overall_similarity_score = factory.LazyAttribute(lambda x: faker.pyfloat())

    security_alignment = factory.LazyAttribute(lambda x: faker.pyfloat(0, 1, True))
    conformity_alignment = factory.LazyAttribute(lambda x: faker.pyfloat(0, 1, True))
    benevolence_alignment = factory.LazyAttribute(lambda x: faker.pyfloat(0, 1, True))
    tradition_alignment = factory.LazyAttribute(lambda x: faker.pyfloat(0, 1, True))
    universalism_alignment = factory.LazyAttribute(lambda x: faker.pyfloat(0, 1, True))
    self_direction_alignment = factory.LazyAttribute(
        lambda x: faker.pyfloat(0, 1, True)
    )
    stimulation_alignment = factory.LazyAttribute(lambda x: faker.pyfloat(0, 1, True))
    hedonism_alignment = factory.LazyAttribute(lambda x: faker.pyfloat(0, 1, True))
    achievement_alignment = factory.LazyAttribute(lambda x: faker.pyfloat(0, 1, True))
    power_alignment = factory.LazyAttribute(lambda x: faker.pyfloat(0, 1, True))

    top_match_percent = factory.LazyAttribute(
        lambda o: as_percent(calculate_alignment_score_top_match(o)[1])
    )
    top_match_value = factory.LazyAttribute(
        lambda o: calculate_alignment_score_top_match(o)[0]
    )

    class Meta:
        model = AlignmentScores


def calculate_alignment_score_top_match(
    alignment_score: AlignmentScores,
) -> typing.Tuple[str, float]:
    alignment_map = dict()
    for personal_value in PersonalValue:
        alignment_map[personal_value.key] = getattr(
            alignment_score, f"{personal_value.key}_alignment"
        )
    return get_max(alignment_map)


class EffectChoiceFactory(factory.alchemy.SQLAlchemyModelFactory):
    effect_choice_uuid = factory.Sequence(lambda x: faker.uuid4().upper())
    effect_choice_1_iri = factory.LazyAttribute(lambda x: faker.pystr(20, 50))

    class Meta:
        model = EffectChoice


class SolutionChoiceFactory(factory.alchemy.SQLAlchemyModelFactory):
    solution_choice_uuid = factory.Sequence(lambda x: faker.uuid4().upper())
    solution_choice_1_iri = factory.LazyAttribute(lambda x: faker.pystr(20, 50))
    solution_choice_2_iri = factory.LazyAttribute(lambda x: faker.pystr(20, 50))

    class Meta:
        model = SolutionChoice


class AlignmentFeedFactory(factory.alchemy.SQLAlchemyModelFactory):
    alignment_feed_uuid = factory.Sequence(lambda x: faker.uuid4().upper())

    aligned_effect_1_iri = factory.LazyAttribute(lambda x: faker.pystr(20, 50))
    aligned_effect_2_iri = factory.LazyAttribute(lambda x: faker.pystr(20, 50))
    aligned_effect_3_iri = factory.LazyAttribute(lambda x: faker.pystr(20, 50))

    aligned_solution_1_iri = factory.LazyAttribute(lambda x: faker.pystr(20, 50))
    aligned_solution_2_iri = factory.LazyAttribute(lambda x: faker.pystr(20, 50))
    aligned_solution_3_iri = factory.LazyAttribute(lambda x: faker.pystr(20, 50))
    aligned_solution_4_iri = factory.LazyAttribute(lambda x: faker.pystr(20, 50))
    aligned_solution_5_iri = factory.LazyAttribute(lambda x: faker.pystr(20, 50))
    aligned_solution_6_iri = factory.LazyAttribute(lambda x: faker.pystr(20, 50))
    aligned_solution_7_iri = factory.LazyAttribute(lambda x: faker.pystr(20, 50))

    class Meta:
        model = AlignmentFeed


class UserBJourneyFactory(factory.alchemy.SQLAlchemyModelFactory):
    conversation = factory.SubFactory(ConversationsFactory)
    quiz = factory.SubFactory(ScoresFactory)
    alignment_scores = factory.SubFactory(AlignmentScoresFactory)
    alignment_feed = factory.SubFactory(AlignmentFeedFactory)
    effect_choice = factory.SubFactory(EffectChoiceFactory)
    solution_choice = factory.SubFactory(SolutionChoiceFactory)
    consent = factory.LazyAttribute(lambda obj: obj.conversation.user_b_share_consent)

    class Meta:
        model = UserBJourney
