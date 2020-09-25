from knowledge_graph import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from knowledge_graph import login


""" Contains all of the table structures for the database. When these are updated
    two commands need to be run in terminal/console.

    1) flask db migrate -m "leave a comment about changes here"
    2) flask db upgrade

    This ensures that the database models are updated and ready to use.
"""


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    zip = db.Column(db.Integer, db.ForeignKey("zip.zip"))
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
    return User.query.get(int(id))


class Scores(db.Model):
    session_id = db.Column(db.String, db.ForeignKey("user.id"), primary_key=True)
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


class Iri(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    iri = db.Column(db.String(120), unique=True)
    zips = db.relationship("Zip", secondary="lrf")

    def __repr__(self):
        """ Tells Python how to print """
        return "<IRI {}>".format(self.iri)


class Zip(db.Model):
    zip = db.Column(db.Integer, primary_key=True)
    users = db.relationship("User", backref="lives_in", lazy="dynamic")
    iris = db.relationship("Iri", secondary="lrf")

    def __repr__(self):
        """ Tells Python how to print """
        return "<Zip {}>".format(self.zip)


class Lrf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zip_id = db.Column(db.Integer, db.ForeignKey("zip.zip"))
    iri_id = db.Column(db.Integer, db.ForeignKey("iri.id"))
