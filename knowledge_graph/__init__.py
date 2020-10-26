from flask import Flask
from flask_cors import CORS
from config import BaseConfig, DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_autodoc import Autodoc

app = Flask(__name__)
auto = Autodoc(app)
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"
CORS(app)


from knowledge_graph import routes, models
