import os
from knowledge_graph import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from knowledge_graph import login

# Azure
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


""" Contains all of the table structures for the database. When these are updated
    two commands need to be run in terminal/console.

    1) flask db migrate -m "leave a comment about changes here"
    2) flask db upgrade


    This ensures that the database models are updated and ready to use.
"""

# Begin Azure Connection
# Older code for params -> params = urllib.parse.quote_plus()

# DATABASE_PARAMS = os.environ["DATABASE_PARAMS"]
# SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % DATABASE_PARAMS
# SQLALCHEMY_COMMIT_ON_TEARDOWN = True
# SQLALCHEMY_TRACK_MODIFICATIONS = False
# engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
# Base = declarative_base(engine)

# End Azure Connection

# Temporary local DB
# engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"], echo=True)
# Base = declarative_base(engine)

# End temporary local DB


# Azure DB Models Start
# class Users(UserMixin, Base):
#     """Automatically loads Users table from Azure DB
#
#     Valid Columns
#     -------------
#     user_id -> UUID4 format
#     username -> NVARCHAR(255)
#     email -> NVARCHAR(255)
#     password_hash -> NVARCHAR(255)
#     zip_key -> INT
#     """
#
#     __tablename__ = "Users"
#     __table_args__ = {"autoload": True}
#
#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)
#
#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)
#
#     def __repr__(self):
#         """ Tells Python how to print """
#         return "<User {}>".format(self.username)
#
#
# @login.user_loader
# def load_user(id):
#     return Users.query.get(id)
#
#
# class Scores(Base):
#     """Automatically loads Scores table from Azure DB
#
#     Valid Columns
#     -------------
#     scores_id -> UUID4 format
#     session_id -> UUID4 format
#     user_id -> UUID4 format
#     security -> FLOAT
#     conformity -> FLOAT
#     benevolence -> FLOAT
#     tradition -> FLOAT
#     universalism -> FLOAT
#     self_direction -> FLOAT
#     stimulation -> FLOAT
#     hedonism -> FLOAT
#     achievement -> FLOAT
#     power -> FLOAT
#
#     """
#
#     __tablename__ = "Scores"
#     __table_args__ = {"autoload": True}
#
#
# class Sessions(Base):
#     """Automatically loads Sessions table from Azure DB
#
#     Valid Columns
#     -------------
#     session_id -> UUID4 format
#
#     """
#
#     __tablename__ = "Sessions"
#     __table_args__ = {"autoload": True}
#
#
# def loadSession():
#     """Initializes a database session and connects with Azure.
#
#     THIS IS NOT THE SESSIONS TABLE.
#     """
#     metadata = Base.metadata
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     return session
#
#
# session = loadSession()
#
#
# def getSession():
#     """ This provides other files access to the database session."""
#     return session

# Azure DB Models End

# Temporary local DB start


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
    scores = db.relationship("Scores", backref="owner_of_scores", lazy="dynamic")
    # ip_address = db.Column(db.String(255), primary_key=False)


# create tables in database if they don't exist. Do nothing if they do exist.
# engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

# db.create_all()

# def loadSession():
#     """Initializes a database session and connects with Azure.
#     THIS IS NOT THE SESSIONS TABLE.
#     """
#     metadata = db.Model.metadata
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     return session


# session = loadSession()


# def getSession():
#     """ This provides other files access to the database session."""
#     return session


# Temporary Local DB end
