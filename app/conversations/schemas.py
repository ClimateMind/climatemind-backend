from marshmallow import fields, validate, ValidationError, validates_schema, post_load

from app.common.schemas import CamelCaseSchema, ma
from app.conversations.enums import (
    ConversationState,
    ConversationUserARating,
)
from app.models import Conversations


class ConversationEditSchema(CamelCaseSchema, ma.SQLAlchemySchema):
    class Meta:
        model = Conversations
        load_instance = True

    conversation_id = ma.auto_field("conversation_uuid")
    receiver_name = ma.auto_field()
    state = fields.Integer(
        validate=validate.OneOf([s.value for s in ConversationState])
    )
    user_a_rating = fields.Integer(
        validate=validate.OneOf([s.value for s in ConversationUserARating])
    )

    @validates_schema
    def validate_rating_alongside_with_button_clicked(self, data: dict, **kwargs):
        rating_provided = data.get("user_a_rating") is not None
        button_clicked = data.get("state") is not None
        if rating_provided and button_clicked:
            raise ValidationError(
                "Button click could not be provided with user rating",
                field_name="state",
            )

    @post_load
    def fill_state(self, data: dict, **kwargs):
        if data.get("user_a_rating"):
            data["state"] = ConversationState.RatingDone

        input_state = data.get("state")
        if input_state is not None:
            instance = self.instance or self.get_instance(data)

            if instance and instance.state is not None:
                if instance.state > input_state:
                    raise ValidationError(
                        "Unable to change conversation state backward"
                    )
                elif instance.state == input_state and not data.get("user_a_rating"):
                    raise ValidationError("Conversation is already in this state")

        return data
