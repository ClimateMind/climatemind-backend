from flask import Blueprint

bp = Blueprint("feedback", __name__)

from app.feedback import routes
