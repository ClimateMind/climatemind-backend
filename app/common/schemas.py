from flask import current_app
from flask_marshmallow import Marshmallow
from marshmallow import Schema

from app.errors.errors import InvalidUsageError

ma = Marshmallow(current_app)


def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class CamelCaseSchema:
    """Schema that uses camel-case for its external representation
    and snake-case for its internal representation.
    """

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)


def validate_schema_field(schema: Schema, field_name: str, value: str) -> bool:
    errors = schema.validate({field_name: value}, partial=True)
    if errors:
        raise InvalidUsageError(message=f"{field_name}: {errors[field_name]}")
    else:
        return True
