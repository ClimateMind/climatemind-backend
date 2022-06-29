from flask_caching import Cache
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_selfdoc import Autodoc
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

db = SQLAlchemy(
    metadata=MetaData(
        naming_convention={
            "pk": "pk_%(table_name)s",
            "fk": "fk_%(table_name)s__%(column_0_name)s__%(referred_table_name)s",
            "ix": "ix_%(table_name)s__%(column_0_name)s",
            "uq": "uq_%(table_name)s__%(column_0_name)s",
            "ck": "ck_%(table_name)s__%(constraint_name)s",
        }
    )
)
migrate = Migrate()
login = LoginManager()
login.login_view = "auth.login"
login.login_message = "Please log in to access this page."
cache = Cache()
auto = Autodoc()
jwt = JWTManager()
limiter = Limiter(
    key_func=get_remote_address, default_limits=["1000 per day", "200 per hour"]
)
