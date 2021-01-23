from flask import Blueprint

bp = Blueprint("feed", __name__)

from app.feed import routes
