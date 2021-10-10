from flask import current_app
from app import create_app, db
from app.models import Users, Scores, Sessions  # TODO Lrf, Zip, Iri


app = create_app()
app.app_context().push()
