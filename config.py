from flask import abort
import os

from knowledge_graph.Mind import Mind


class BaseConfig(object):
    DEBUG = False


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
