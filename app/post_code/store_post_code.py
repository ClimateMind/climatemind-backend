import re
from app import db
from app.models import Sessions
from app.errors.errors import DatabaseError


def store_post_code(post_code, session_uuid):
    """
    Post codes are (optionally) given by the user to localise their feed and show the climate change impacts most relevant to where they live.
    A regular expression is used to check whether the post code contains 5 digits.
    If the post code is valid, it is committed to the Sessions table alongside the session_uuid.
    """
    s = Sessions.query.filter_by(session_uuid=session_uuid).first()
    if s:
        try:
            s.postal_code = post_code
            db.session.commit()

            response = {
                "message": "Successfully added post code to the database.",
                "postCode": post_code,
                "sessionId": session_uuid,
            }
            return response, 201
        except:
            raise DatabaseError(
                message="Something went wrong while saving post code to the database."
            )
    else:
        raise DatabaseError(
            message="Cannot save post code. Session id is not in database."
        )


def check_post_code(post_code):
    regex = re.compile(r"(\b\d{5})\b")
    post_code_valid = regex.search(post_code)
    return post_code_valid
