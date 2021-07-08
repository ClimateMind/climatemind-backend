from flask import Blueprint

bp = Blueprint("session", __name__)

from app.session import routes
