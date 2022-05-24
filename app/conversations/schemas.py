from marshmallow import fields, validate

from app.common.schemas import CamelCaseSchema, ma
from app.conversations.enums import ConversationStatus
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
