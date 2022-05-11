import os

from flask import current_app
from jsonschema.exceptions import ValidationError, SchemaError
from jsonschema.validators import validate

from app.personal_values.enums import PersonalValue
from app.personal_values.utils import (
    get_value_descriptions_file_data,
    get_value_descriptions_schema,
)

JSON_FILE = get_value_descriptions_file_data()
JSON_SCHEMA = get_value_descriptions_schema()


def test_value_descriptions_files_exist():
    assert os.path.exists(current_app.config.get("VALUE_DESCRIPTIONS_FILE"))
    assert os.path.exists(current_app.config.get("VALUE_DESCRIPTIONS_SCHEMA"))


def test_check_value_descriptions_personal_values_enum():
    json_schema_desc_object = JSON_SCHEMA["$defs"]["value_description"]

    personal_values_keys = PersonalValue.get_all_keys()
    ids_from_file = json_schema_desc_object["properties"]["id"]["enum"]
    assert set(personal_values_keys) == set(ids_from_file), "Ids are equal to Enum"

    root_obj_requirement_fileds_from_file = JSON_SCHEMA["required"]
    assert set(personal_values_keys) == set(
        root_obj_requirement_fileds_from_file
    ), "Root object requirement fields are equal to Enum keys"

    personal_values_spaced_keys = PersonalValue.get_all_keys(sep=" ")
    names_from_file = json_schema_desc_object["properties"]["name"]["enum"]
    assert set(personal_values_spaced_keys) == set(
        names_from_file
    ), "Names are equal to Enum"


def test_validate_values_descriptions_file_and_schema():
    try:
        validate(JSON_FILE, JSON_SCHEMA)
        assert True, "You will never see ths message."
    except ValidationError:
        assert False, "Value descriptions file is not valid"
    except SchemaError:
        assert False, "Value descriptions schema is not valid"
