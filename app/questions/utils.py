from json import load

from flask import current_app


def get_schwartz_questions_file_data() -> dict:
    return get_dict_from_json_file(current_app.config.get("SCHWARTZ_QUESTIONS_FILE"))


def get_schwartz_questions_schema() -> dict:
    return get_dict_from_json_file(current_app.config.get("SCHWARTZ_QUESTIONS_SCHEMA"))


def get_dict_from_json_file(json_file_name: str) -> dict:
    with open(json_file_name) as json_file:
        data = load(json_file)
    return data
