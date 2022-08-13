import sentry_sdk
from flask import Flask
from flask_cors import CORS
from sentry_sdk.integrations.flask import FlaskIntegration

from app import models
from app.extensions import db, migrate, login, cache, auto, jwt, limiter
from config import DevelopmentConfig


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    init_sentry(app)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    cache.init_app(app)
    auto.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)

    origins = {
        "origins": [
            "http://127.0.0.1:3000",
            "http://localhost:3000",
            "http://0.0.0.0:3000",
            "https://app-frontend-test-001.azurewebsites.net:80",
            "https://app-frontend-prod-001.azurewebsites.net:80",
            "https://app.climatemind.org:80",
        ]
    }

    CORS(
        app,
        resources={
            r"/refresh": origins,
            r"/login": origins,
            r"/password-reset": origins,
            r"/register": origins,
            r"/logout": origins,
            r"/captcha": origins,
            r"/email": origins,
            r"/alignment": origins,
        },
        supports_credentials=True,
    )

    with app.app_context():

        from app.auth import bp as auth_bp

        app.register_blueprint(auth_bp)

        from app.errors import bp as errors_bp

        app.register_blueprint(errors_bp)

        from app.subscribe import bp as subscribe_bp

        app.register_blueprint(subscribe_bp)

        from app.feed import bp as feed_bp

        app.register_blueprint(feed_bp)

        from app.myths import bp as myths_bp

        app.register_blueprint(myths_bp)

        from app.solutions import bp as solutions_bp

        app.register_blueprint(solutions_bp)

        from app.scoring import bp as scoring_bp

        app.register_blueprint(scoring_bp)

        from app.questions import bp as questions_bp

        app.register_blueprint(questions_bp)

        from app.personal_values import bp as personal_values_bp

        app.register_blueprint(personal_values_bp)

        from app.documentation import bp as documentation_bp

        app.register_blueprint(documentation_bp)

        from app.post_code import bp as post_code_bp

        app.register_blueprint(post_code_bp)

        from app.session import bp as session_bp

        app.register_blueprint(session_bp)

        from app.account import bp as email_bp

        app.register_blueprint(email_bp)

        from app.conversations import bp as conversations_bp

        app.register_blueprint(conversations_bp)

        from app.alignment import bp as alignment_bp

        app.register_blueprint(alignment_bp)

        from app.user_b import bp as user_b_bp

        app.register_blueprint(user_b_bp)

        from app.ontology import bp as ontology_bp

        app.register_blueprint(ontology_bp)

    return app


def init_sentry(app):
    dsn = app.config.get("SENTRY_DSN")
    environment = app.config.get("SENTRY_ENVIRONMENT")

    if dsn and environment:
        try:
            traces_sample_rate = float(app.config.get("SENTRY_TRACES_SAMPLE_RATE"))
        except (ValueError, TypeError):
            traces_sample_rate = 0.1

        sentry_sdk.init(
            dsn=dsn,
            integrations=[
                FlaskIntegration(),
            ],
            traces_sample_rate=traces_sample_rate,
            environment=environment,
            send_default_pii=True,
            attach_stacktrace=True,
        )
