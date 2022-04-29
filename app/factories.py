import random

import factory
from faker import Factory as FakerFactory
from werkzeug.security import generate_password_hash

from app.conversations.routes import ConversationStatus
from app.models import Users, Sessions, Scores, Conversations, AlignmentScores
from app.personal_values.enums import PersonalValue

faker = FakerFactory.create()


class UsersFactory(factory.alchemy.SQLAlchemyModelFactory):
    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_name = factory.LazyAttribute(lambda x: faker.last_name())
    user_uuid = factory.LazyAttribute(lambda x: faker.uuid4().upper())
    user_email = factory.LazyAttribute(lambda x: faker.email())
    password = factory.LazyAttribute(lambda x: faker.password())
    password_hash = factory.LazyAttribute(lambda o: generate_password_hash(o.password))

    class Meta:
        model = Users
        exclude = ("password",)


class SessionsFactory(factory.alchemy.SQLAlchemyModelFactory):
    ip_address = factory.LazyAttribute(lambda x: faker.ipv4())
    user = factory.SubFactory(UsersFactory)
    session_uuid = factory.LazyAttribute(lambda x: faker.uuid4().upper())
    session_created_timestamp = factory.LazyAttribute(lambda x: faker.date_time())

    class Meta:
        model = Sessions


class ScoresFactory(factory.alchemy.SQLAlchemyModelFactory):
    quiz_uuid = factory.LazyAttribute(lambda x: faker.uuid4().upper())
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
    conversation_uuid = factory.LazyAttribute(lambda x: faker.uuid4().upper())
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
    alignment_scores_uuid = factory.LazyAttribute(lambda x: faker.uuid4().upper())
    overall_similarity_score = factory.LazyAttribute(lambda x: faker.pyfloat())
    top_match_percent = factory.LazyAttribute(lambda x: faker.pyfloat(0, 2, True))
    top_match_value = factory.LazyAttribute(
        lambda x: random.choice([v.key for v in PersonalValue])
    )

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

    class Meta:
        model = AlignmentScores
