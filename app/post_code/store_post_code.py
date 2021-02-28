import re

from app import db
from app.models import Sessions


def store_post_code(post_code, session_uuid):
    """
    Post codes are (optionally) given by the user to localise their feed and show the climate change impacts most relevant to where they live.
    A regular expression is used to check whether the post code contains 5 digits.
    If the post code is valid, it is committed to the Sessions table alongside the session_uuid.
    """
    regex = re.compile(r"(\b\d{5})\b")
    post_code_valid = regex.search(post_code)

    if post_code_valid:
        try:
            s = Sessions.query.filter_by(session_uuid=session_uuid).first()
        except:
            return {"error": "Error querying the database"}, 500

        s.postal_code = post_code

        try:
            db.session.commit()

            response = {
                "message": "Successfully added post code",
                "postCode": post_code,
                "sessionId": session_uuid,
            }

            return response, 201

        except:
            return {"error": "Error saving to the database"}, 500

    else:
        return {"error": "Invalid Postal Code"}, 500
