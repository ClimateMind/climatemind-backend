from marshmallow import fields, validate, ValidationError, validates_schema, post_load
from marshmallow_enum import EnumField

from app.common.schemas import CamelCaseSchema, ma
from app.conversations.enums import (
    ConversationStatus,
    ConversationButtonMapState,
    ConversationState,
    ConversationUserARating,
)
from app.models import Conversations


class ConversationEditSchema(CamelCaseSchema, ma.SQLAlchemySchema):
    class Meta:
        model = Conversations
        load_instance = True

    # FIXME: deprecated
    conversation_status = fields.Integer(
        validate=validate.OneOf([s.value for s in ConversationStatus])
    )

    conversation_id = ma.auto_field("conversation_uuid")
    receiver_name = ma.auto_field()
    state = ma.auto_field(dump_only=True)
    button_clicked = EnumField(ConversationButtonMapState, load_only=True)
    user_a_rating = fields.Integer(
        validate=validate.OneOf([s.value for s in ConversationUserARating])
    )

    @validates_schema
    def validate_rating_alongside_with_button_clicked(self, data: dict, **kwargs):
        rating_provided = data.get("user_a_rating") is not None
        button_clicked = data.get("button_clicked") is not None
        if rating_provided and button_clicked:
            raise ValidationError(
                "Button click could not be provided with rating",
                field_name="button_clicked",
            )

    @post_load
    def fill_state(self, data: dict, **kwargs):
        if data.get("user_a_rating"):
            data["state"] = ConversationState.RatingDone
        else:
            try:
                button_clicked_value = data.pop("button_clicked")
                data["state"] = button_clicked_value
            except KeyError:
                pass

        input_state = data.get("state")
        if input_state:
            instance = self.instance or self.get_instance(data)

            if instance and instance.state is not None:
                if instance.state > input_state:
                    raise ValidationError(
                        "Unable to change conversation state backward"
                    )
                elif instance.state == input_state:
                    raise ValidationError("Conversation is already in this state")

        return data
