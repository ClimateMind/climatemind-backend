from app import create_app

app = create_app()
app.app_context().push()


from flask import request
from app.session.session_helpers import maybe_assign_session


@app.before_request
def before_request_hook():
    maybe_assign_session(request)
