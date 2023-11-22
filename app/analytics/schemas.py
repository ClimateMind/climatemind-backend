from marshmallow import (
    Schema,
    fields,
    validates_schema,
    ValidationError,
)

from app.common.schemas import CamelCaseSchema


class AnalyticsSchema(CamelCaseSchema, Schema):
    category = fields.Str(required=True)
    action = fields.Str(required=True)
    label = fields.Str(required=True)
    event_value = fields.Str(required=True)
    event_timestamp = fields.Datetime(required=True)
    page_url = fields.Str(required=True)
