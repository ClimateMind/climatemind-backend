from flask import current_app

from app.common.static import get_dict_from_json_file


def get_schwartz_questions_file_data() -> dict:
    return get_dict_from_json_file(current_app.config.get("SCHWARTZ_QUESTIONS_FILE"))


def get_schwartz_questions_schema() -> dict:
    return get_dict_from_json_file(current_app.config.get("SCHWARTZ_QUESTIONS_SCHEMA"))
