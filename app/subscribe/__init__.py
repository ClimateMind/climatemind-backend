from flask import Blueprint

bp = Blueprint("subscribe", __name__)

from app.subscribe import routes
