class BaseConfig(object):
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    try:
        app.config["MIND"] = Mind()
    except (FileNotFoundError, IsADirectoryError, ValueError):
        abort(404)


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    # todo: add mock mind here