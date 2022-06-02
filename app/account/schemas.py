from marshmallow import (
    Schema,
    fields,
    validates_schema,
    ValidationError,
)

from app.auth.validators import password_valid
from app.common.schemas import CamelCaseSchema


class UserChangePasswordSchema(CamelCaseSchema, Schema):
    current_password = fields.Str()
    new_password = fields.Str(validate=password_valid)
    confirm_password = fields.Str()

    @validates_schema
    def validate_confirm_password(self, data, **kwargs):
        if data["new_password"] != data["confirm_password"]:
            raise ValidationError(
                "Passwords are not equal", field_name="confirm_password"
            )
