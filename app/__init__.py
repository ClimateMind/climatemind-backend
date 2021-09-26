from app import models
from flask import Flask
from datetime import datetime
from datetime import timezone
from datetime import timedelta
from flask_cors import CORS
from app.extensions import db, migrate, login, cache, auto, jwt, limiter
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import set_access_cookies

from config import DevelopmentConfig


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

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
            r"/register": origins,
            r"/logout": origins,
            r"/captcha": origins,
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

        from app.conversations import bp as conversations_bp

        app.register_blueprint(conversations_bp)

    return app
