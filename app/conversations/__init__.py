from flask import Blueprint

bp = Blueprint("conversations", __name__)

from app.conversations import routes
