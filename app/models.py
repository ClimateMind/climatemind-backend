import os
from flask import current_app
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
    # postal code variable type for SQL will need to change when scaling up allow longer postal codes
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

    @classmethod
    def get_scores_list(cls, session_uuid):
        """
        Alphabetically organized lists of scores are needed when performing
        vector operations.

        :params session_uuid: uuid4 as str
        :returns user_uuid: uuid4 as str
        :returns scores_list: alphabetically ordered
        """
        personal_values_categories = [
            "achievement",
            "benevolence",
            "conformity",
            "hedonism",
            "power",
            "security",
            "self_direction",
            "stimulation",
            "tradition",
            "universalism",
        ]

        scores = (
            db.session.query(Scores)
            .join(Sessions)
            .filter(Scores.session_uuid == session_uuid)
            .one_or_none()
        )

        if not scores:
            return None, None

        user_uuid = scores.user_uuid

        scores_dict = scores.__dict__
        scores_list = [scores_dict[key] for key in personal_values_categories]
        return user_uuid, scores_list


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
    receiver_session_uuid = db.Column(
        UNIQUEIDENTIFIER,
        db.ForeignKey("sessions.session_uuid"),
        index=False,
        unique=False,
        nullable=True,
    )
    receiver_name = db.Column(db.String(50), index=False, unique=False, nullable=False)
    conversation_status = db.Column(db.Integer)
    conversation_created_timestamp = db.Column(db.DateTime)


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
