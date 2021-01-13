import os
from knowledge_graph import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from knowledge_graph import login

# Azure
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


""" Contains all of the table structures for the database.
    Migrations need to be run when changes are made.
"""


class Users(UserMixin, db.Model):
    user_id = db.Column(db.String(256), primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
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
    return User.query.get(Int(id))


class Scores(db.Model):
    scores_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_id = db.Column(db.String(256), db.ForeignKey("sessions.session_id"))
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
    user_id = db.Column(db.String(256), db.ForeignKey("users.user_id"))


class Sessions(db.Model):
    session_id = db.Column(db.String(256), primary_key=True)
    # postal code variable type for SQL will need to change when scaling up to accept longer postal codes
    postal_code = db.Column(db.String(5))
    scores = db.relationship("Scores", backref="owner_of_scores", lazy="dynamic")
    ip_address = db.Column(db.String(255), primary_key=False)


class Signup(db.Model):
    email = db.Column(db.String(254), primary_key=True)
    session_id = db.Column(db.String(256), db.ForeignKey("sessions.session_id"))
    signup_timestamp = db.Column(db.DateTime)


class ClimateFeed(db.Model):
    climate_feed_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_id = db.Column(db.String(256), db.ForeignKey("sessions.session_id"))
    event_ts = db.Column(db.DateTime)
    effect_position = db.Column(db.Integer)
    effect_iri = db.Column(db.String(255))
    effect_score = db.Column(db.Float)
    solution_1_iri = db.Column(db.String(255))
    solution_2_iri = db.Column(db.String(255))
    solution_3_iri = db.Column(db.String(255))
    solution_4_iri = db.Column(db.String(255))
    isPossiblyLocal = db.Column(db.Boolean)
