from marshmallow import fields, validate

from app.common.schemas import CamelCaseSchema, ma
from app.conversations.enums import ConversationStatus, ConversationState
from app.models import Conversations


class ConversationEditSchema(CamelCaseSchema, ma.SQLAlchemySchema):
    class Meta:
        model = Conversations
        load_instance = True

    conversation_id = ma.auto_field("conversation_uuid")
    receiver_name = ma.auto_field()
    conversation_status = fields.Integer(
        validate=validate.OneOf([s.value for s in ConversationStatus])
    )
    state = fields.Integer(
        validate=validate.OneOf([s.value for s in ConversationState])
    )
    rating_levels = 5  # TODO: this constant should probably be elsewhere?
    user_a_rating = fields.Integer(
        validate=validate.OneOf(list(range(rating_levels)))  # TODO: would an enum be better here too, even though ratings are naturally just integers?
    )
