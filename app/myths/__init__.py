from flask import Blueprint

bp = Blueprint("myths", __name__)

from app.myths import routes
