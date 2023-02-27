from app.common.schemas import ma
from app.models import Feedback


class FeedbackSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Feedback
        load_instance = True

    text = ma.auto_field()
