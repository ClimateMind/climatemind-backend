import uuid
from app import db
from app.errors.errors import DatabaseError
from app.models import AnalyticsData
from datetime import datetime, timezone


def log_user_a_event(
    session_uuid, category, action, label, event_value, event_timestamp, page_url
):
    """
    Log an event in the user a analytics data table.
    """
    try:
        event_to_add = AnalyticsData()

        # event_to_add.event_log_uuid = uuid.uuid4() #this should not be needed as autoincrement is set to true.
        event_to_add.session_uuid = session_uuid
        event_to_add.category = category
        event_to_add.action = action
        event_to_add.label = label
        event_to_add.value = event_value
        event_to_add.event_timestamp = datetime.strptime(
            str(event_timestamp), "%Y-%m-%d %H:%M:%S"
        )
        event_to_add.page_url = page_url
        # event_to_add.event_timestamp = datetime.now(timezone.utc)
        db.session.add(event_to_add)
        db.session.commit()
    except:
        raise DatabaseError(
            message="An error occurred while logging a user analytics event."
        )
