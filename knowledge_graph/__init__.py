from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../db/development.db"
db = SQLAlchemy(app)

from knowledge_graph import routes, config

