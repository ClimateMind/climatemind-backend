import os

from flask import current_app
from jsonschema.exceptions import ValidationError, SchemaError
from jsonschema.validators import validate

from app.personal_values.enums import PersonalValue, DEFAULT_SEPARATOR
from app.questions.utils import (
    get_schwartz_questions_file_data,
    get_schwartz_questions_schema,
)

JSON_SCHEMA = get_schwartz_questions_schema()
JSON_FILE = get_schwartz_questions_file_data()


def test_schwartz_questions_files_exist():
    assert os.path.exists(current_app.config.get("SCHWARTZ_QUESTIONS_FILE"))
    assert os.path.exists(current_app.config.get("SCHWARTZ_QUESTIONS_SCHEMA"))


def test_check_schwartz_questions_personal_values_enum():
    personal_values = PersonalValue.get_all_keys(sep="-")
    enum_from_file = JSON_SCHEMA["$defs"]["question"]["properties"]["value"]["enum"]
    assert set(personal_values) == set(enum_from_file)


def test_schwartz_questions_set_one_ids_equal_to_personal_value_ids():
    set_one = JSON_FILE["SetOne"]
    for json_personal_value in set_one:
        raw_name = json_personal_value["value"]
        enum_name = raw_name.upper().replace("-", DEFAULT_SEPARATOR)
        assert PersonalValue[enum_name] == json_personal_value["id"]


def test_validate_schwartz_questions_file_and_schema():
    try:
        validate(JSON_FILE, JSON_SCHEMA)
        assert True, "You will never see ths message."
    except ValidationError:
        assert False, "Schwartz questions file is not valid"
    except SchemaError:
        assert False, "Schwartz questions schema is not valid"
