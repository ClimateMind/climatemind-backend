from flask import Blueprint

bp = Blueprint("ontology", __name__)

from app.ontology.commands import *
