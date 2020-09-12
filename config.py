from flask import abort
import os

from knowledge_graph.Mind import Mind

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    try:
        MIND = Mind()
    except (FileNotFoundError, IsADirectoryError, ValueError):
        abort(404)


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    # todo: add mock mind here
