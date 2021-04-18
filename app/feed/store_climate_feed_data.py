from app import db
from app.models import ClimateFeed
import datetime
from datetime import timezone
from app.errors.errors import DatabaseError


def store_climate_feed_data(session_uuid, feed):
    try:
        dt = datetime.datetime.now(timezone.utc)
        for i in range(len(feed)):
            effect = ClimateFeed()
            effect.session_uuid = session_uuid
            effect.event_timestamp = dt
            effect.effect_position = i + 1
            effect.effect_iri = feed[i]["effectId"]
            effect.effect_score = feed[i]["effectScore"]
            solutions = feed[i]["effectSolutions"]

            for i in range(len(solutions)):
                iri = solutions[i]["iri"]
                column_name = "solution_" + str(i + 1) + "_iri"
                setattr(effect, column_name, iri)

            effect.isPossiblyLocal = feed[i]["isPossiblyLocal"]

            db.session.add(effect)
            db.session.commit()
    except:
        raise DatabaseError(
            message="An error occurred while saving the feed to database."
        )
