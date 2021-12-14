import os
from flask import current_app
from sqlalchemy.orm.session import close_all_sessions
from app.extensions import db, jwt
from werkzeug.security import generate_password_hash, check_password_hash

# Azure
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER


""" Contains all of the table structures for the database.
    Migrations need to be run when changes are made.
"""


class Sessions(db.Model):
    __tablename__ = "sessions"
    ip_address = db.Column(db.String(255), primary_key=False)
    user_uuid = db.Column(UNIQUEIDENTIFIER, db.ForeignKey("users.user_uuid"))
    session_uuid = db.Column(UNIQUEIDENTIFIER, primary_key=True)
    session_created_timestamp = db.Column(db.DateTime)


class Users(db.Model):
    __tablename__ = "users"
    user_uuid = db.Column(UNIQUEIDENTIFIER, primary_key=True)
    user_email = db.Column(db.String(120), index=True, unique=True)
    user_created_timestamp = db.Column(db.DateTime)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(50), index=False, unique=False, nullable=False)
    last_name = db.Column(db.String(50), index=False, unique=False, nullable=False)
    quiz_uuid = db.Column(UNIQUEIDENTIFIER, db.ForeignKey("scores.quiz_uuid"))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(user_email=email).one_or_none()
        return user

    def __repr__(self):
        """Tells Python how to print"""
        return "<User {}>".format(self.user_email)


@jwt.user_identity_loader
def user_identity_lookup(user):
    """
    Register a callback function that takes whatever object is passed in as the
    identity when creating JWTs and converts it to a JSON serializable format.
    """
    return user.user_uuid


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """
    Register a callback function that loades a user from your database whenever
    a protected route is accessed. This should return any python object on a
    successful lookup, or None if the lookup failed for any reason (for example
    if the user has been deleted from the database).
    """
    identity = jwt_data["sub"]
    return Users.query.filter_by(user_uuid=identity).one_or_none()


class Scores(db.Model):
    __tablename__ = "scores"
    quiz_uuid = db.Column(UNIQUEIDENTIFIER, primary_key=True)
    security = db.Column(db.Float, index=False, unique=False)
    conformity = db.Column(db.Float, index=False, unique=False)
    benevolence = db.Column(db.Float, index=False, unique=False)
    tradition = db.Column(db.Float, index=False, unique=False)
    universalism = db.Column(db.Float, index=False, unique=False)
    self_direction = db.Column(db.Float, index=False, unique=False)
    stimulation = db.Column(db.Float, index=False, unique=False)
    hedonism = db.Column(db.Float, index=False, unique=False)
    achievement = db.Column(db.Float, index=False, unique=False)
    power = db.Column(db.Float, index=False, unique=False)
    scores_created_timestamp = db.Column(db.DateTime)
    session_uuid = db.Column(UNIQUEIDENTIFIER, db.ForeignKey("sessions.session_uuid"))
    postal_code = db.Column(db.String(5))


class Signup(db.Model):
    __tablename__ = "signup"
    signup_email = db.Column(db.String(254))
    signup_timestamp = db.Column(db.DateTime)
    session_uuid = db.Column(UNIQUEIDENTIFIER, db.ForeignKey("sessions.session_uuid"))
    signup_id = db.Column(db.Integer, autoincrement=True, primary_key=True)


class ClimateFeed(db.Model):
    __tablename__ = "climate_feed"
    climate_feed_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_timestamp = db.Column(db.DateTime)
    effect_position = db.Column(db.Integer)
    effect_iri = db.Column(db.String(255))
    effect_score = db.Column(db.Float)
    solution_1_iri = db.Column(db.String(255))
    solution_2_iri = db.Column(db.String(255))
    solution_3_iri = db.Column(db.String(255))
    solution_4_iri = db.Column(db.String(255))
    isPossiblyLocal = db.Column(db.Boolean)
    session_uuid = db.Column(UNIQUEIDENTIFIER, db.ForeignKey("sessions.session_uuid"))


class Conversations(db.Model):
    __tablename__ = "conversations"
    conversation_uuid = db.Column(UNIQUEIDENTIFIER, primary_key=True)
    sender_user_uuid = db.Column(
        UNIQUEIDENTIFIER, db.ForeignKey("users.user_uuid"), index=True, nullable=False
    )
    sender_session_uuid = db.Column(
        UNIQUEIDENTIFIER, db.ForeignKey("sessions.session_uuid"), nullable=False
    )
    receiver_name = db.Column(db.String(50), index=False, unique=False, nullable=False)
    conversation_status = db.Column(db.Integer)
    conversation_created_timestamp = db.Column(db.DateTime)
    user_b_share_consent = db.Column(db.Boolean)


class AnalyticsData(db.Model):
    __tablename__ = "analytics_data"
    analytics_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(50))
    action = db.Column(db.String(50))
    label = db.Column(db.String(50))
    session_uuid = db.Column(UNIQUEIDENTIFIER)
    event_timestamp = db.Column(db.DateTime)
    value = db.Column(db.String(255))
    page_url = db.Column(db.String(255))


class UserBAnalyticsData(db.Model):
    __tablename__ = "user_b_analytics_data"
    event_log_uuid = db.Column(UNIQUEIDENTIFIER, primary_key=True)
    conversation_uuid = db.Column(
        UNIQUEIDENTIFIER, db.ForeignKey("conversations.conversation_uuid")
    )
    event_type = db.Column(db.String(255))
    event_value = db.Column(db.String(255))
    event_timestamp = db.Column(db.DateTime)
    event_value_type = db.Column(db.String(255))
    session_uuid = db.Column(UNIQUEIDENTIFIER, db.ForeignKey("sessions.session_uuid"))


class AlignmentScores(db.Model):
    __tablename__ = "alignment_scores"
    alignment_scores_uuid = db.Column(UNIQUEIDENTIFIER, primary_key=True)
    overall_similarity_score = db.Column(db.Float)
    top_match_percent = db.Column(db.Float)
    top_match_value = db.Column(db.String(255))
    security_alignment = db.Column(db.Float)
    conformity_alignment = db.Column(db.Float)
    benevolence_alignment = db.Column(db.Float)
    tradition_alignment = db.Column(db.Float)
    universalism_alignment = db.Column(db.Float)
    self_direction_alignment = db.Column(db.Float)
    stimulation_alignment = db.Column(db.Float)
    hedonism_alignment = db.Column(db.Float)
    achievement_alignment = db.Column(db.Float)
    power_alignment = db.Column(db.Float)


class AlignmentFeed(db.Model):
    __tablename__ = "alignment_feed"
    alignment_feed_uuid = db.Column(UNIQUEIDENTIFIER, primary_key=True)
    aligned_effect_1_iri = db.Column(db.String(255))
    aligned_effect_2_iri = db.Column(db.String(255))
    aligned_effect_3_iri = db.Column(db.String(255))
    aligned_solution_1_iri = db.Column(db.String(255))
    aligned_solution_2_iri = db.Column(db.String(255))
    aligned_solution_3_iri = db.Column(db.String(255))
    aligned_solution_4_iri = db.Column(db.String(255))
    aligned_solution_5_iri = db.Column(db.String(255))
    aligned_solution_6_iri = db.Column(db.String(255))
    aligned_solution_7_iri = db.Column(db.String(255))


class EffectChoice(db.Model):
    _tablename__ = "effect_choice"
    effect_choice_uuid = db.Column(UNIQUEIDENTIFIER, primary_key=True)
    effect_choice_1_iri = db.Column(db.String(255))


class SolutionChoice(db.Model):
    __tablename__ = "solution_choice"
    solution_choice_uuid = db.Column(UNIQUEIDENTIFIER, primary_key=True)
    solution_choice_1_iri = db.Column(db.String(255))
    solution_choice_2_iri = db.Column(db.String(255))


class UserBJourney(db.Model):
    __tablename__ = "user_b_journey"
    conversation_uuid = db.Column(
        UNIQUEIDENTIFIER,
        db.ForeignKey("conversations.conversation_uuid"),
        primary_key=True,
    )
    quiz_uuid = db.Column(UNIQUEIDENTIFIER, db.ForeignKey("scores.quiz_uuid"))
    alignment_scores_uuid = db.Column(
        UNIQUEIDENTIFIER, db.ForeignKey("alignment_scores.alignment_scores_uuid")
    )
    alignment_feed_uuid = db.Column(
        UNIQUEIDENTIFIER, db.ForeignKey("alignment_feed.alignment_feed_uuid")
    )
    effect_choice_uuid = db.Column(
        UNIQUEIDENTIFIER, db.ForeignKey("effect_choice.effect_choice_uuid")
    )
    solution_choice_uuid = db.Column(
        UNIQUEIDENTIFIER, db.ForeignKey("solution_choice.solution_choice_uuid")
    )
    consent = db.Column(db.Boolean)
