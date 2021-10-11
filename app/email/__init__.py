from flask import Blueprint

bp = Blueprint("email", __name__)

from app.email import routes
