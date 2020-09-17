from typing import Type

from knowledge_graph import db
from knowledge_graph.models import User, Scores


def persist_scores(scores: dict) -> Type[KeyError]:
    try:

        u = User()
        u.id = scores['session-id']

        db.session.add(u)
        db.session.commit()

        for key, value in scores:
            s = Scores()

            s.name = key
            s.user_id = scores['session-id']

            s.score = value

            db.session.add(s)
            db.session.commit()

    except KeyError:
        return KeyError
