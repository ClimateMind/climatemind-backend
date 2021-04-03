import datetime
from datetime import timezone
from typing import Type

from app import db
from app.models import Scores, Sessions


def persist_scores(scores):
    """
    Saves user scores and session id into the database

    Args: scores
        scores: A dictionary mapping personal values to user scores

    Returns: An error if one occurs

    """
    try:
        # db.session = getSession()

        userSession = Sessions()
        userSession.session_uuid = scores["session-id"]

        db.session.add(userSession)
        # db.session.commit()

        userScores = Scores()
        userScores.session_uuid = scores["session-id"]
        userScores.security = scores["security"]
        userScores.conformity = scores["conformity"]
        userScores.benevolence = scores["benevolence"]
        userScores.tradition = scores["tradition"]
        userScores.universalism = scores["universalism"]
        userScores.self_direction = scores["self-direction"]
        userScores.stimulation = scores["stimulation"]
        userScores.hedonism = scores["hedonism"]
        userScores.achievement = scores["achievement"]
        userScores.power = scores["power"]
        userScores.scores_created_timestamp = datetime.datetime.now(timezone.utc)

        db.session.add(userScores)
        db.session.commit()

    except:
        abort(500, description="Unable to save provided question data")
