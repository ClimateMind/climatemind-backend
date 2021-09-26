import re
from app import db
from app.models import Scores
from app.errors.errors import DatabaseError


def store_post_code(post_code, quiz_uuid):
    """
    Post codes are (optionally) given by the user to localise their feed and show the climate change impacts most relevant to where they live.
    A regular expression is used to check whether the post code contains 5 digits.
    If the post code is valid, it is committed to the Scores table.
    """
    s = Scores.query.filter_by(quiz_uuid=quiz_uuid).first()
    try:
        s.postal_code = post_code
        db.session.commit()

        response = {
            "message": "Successfully added postal code to the database.",
            "postCode": post_code,
            "quizId": quiz_uuid,
        }
        return response, 201
    except:
        raise DatabaseError(
            message="Something went wrong while saving post code to the database."
        )


def check_post_code(post_code):
    regex = re.compile(r"(\b\d{5})\b")
    post_code_valid = regex.search(post_code)
    return post_code_valid
