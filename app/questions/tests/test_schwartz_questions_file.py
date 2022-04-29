import os

from flask import current_app
from jsonschema.exceptions import ValidationError, SchemaError
from jsonschema.validators import validate

from app.personal_values.enums import PersonalValue
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
    personal_values = [v.dashed_key for v in PersonalValue]
    enum_from_file = JSON_SCHEMA["$defs"]["question"]["properties"]["value"]["enum"]
    assert set(personal_values) == set(enum_from_file)


def test_validate_schwartz_question_file_and_schema():
    try:
        validate(JSON_FILE, JSON_SCHEMA)
        assert True, "You will never see ths message."
    except ValidationError:
        assert False, "Schwartz questions file is not valid"
    except SchemaError:
        assert False, "Schwartz questions schema is not valid"
