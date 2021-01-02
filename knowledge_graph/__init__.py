from flask import Flask
from flask_selfdoc import Autodoc
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

from config import DevelopmentConfig

app = Flask(__name__)
cache = Cache()
auto = Autodoc(app)
app.config.from_object(DevelopmentConfig)
cache.init_app(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"
CORS(app)


from knowledge_graph import routes, models
