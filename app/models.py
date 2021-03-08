import os
from flask import current_app
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

# Azure
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER


""" Contains all of the table structures for the database.
    Migrations need to be run when changes are made.
"""


class Users(UserMixin, db.Model):
    username = db.Column(db.String(64), index=True, unique=True)
    user_created_timestamp = db.Column(db.DateTime)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    user_uuid = db.Column(UNIQUEIDENTIFIER, primary_key=True)
    scores = db.relationship("Scores", backref="owner", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """ Tells Python how to print """
        return "<User {}>".format(self.username)


@login.user_loader
def load_user(id):
    return Users.query.get(id)


class Scores(db.Model):
    scores_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
    user_uuid = db.Column(UNIQUEIDENTIFIER, db.ForeignKey("users.user_uuid"))
    scores_created_timestamp = db.Column(db.DateTime)
    session_uuid = db.Column(UNIQUEIDENTIFIER, db.ForeignKey("sessions.session_uuid"))


class Sessions(db.Model):
    # postal code variable type for SQL will need to change when scaling up to accept longer postal codes
    postal_code = db.Column(db.String(5))
    scores = db.relationship("Scores", backref="owner_of_scores", lazy="dynamic")
    ip_address = db.Column(db.String(255), primary_key=False)
    session_uuid = db.Column(UNIQUEIDENTIFIER, primary_key=True)


class Signup(db.Model):
    email = db.Column(db.String(254))
    signup_timestamp = db.Column(db.DateTime)
    session_uuid = db.Column(UNIQUEIDENTIFIER, db.ForeignKey("sessions.session_uuid"))
    signup_id = db.Column(db.Integer, autoincrement=True, primary_key=True)


class ClimateFeed(db.Model):
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


class AnalyticsData(db.Model):
    analytics_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(50))
    action = db.Column(db.String(50))
    label = db.Column(db.String(50))
    session_uuid = db.Column(UNIQUEIDENTIFIER)
    event_timestamp = db.Column(db.DateTime)
    value = db.Column(db.String(255))
