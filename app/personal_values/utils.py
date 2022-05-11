from flask import current_app

from app.common.static import get_dict_from_json_file


def get_value_descriptions_file_data() -> dict:
    return get_dict_from_json_file(current_app.config.get("VALUE_DESCRIPTIONS_FILE"))


def get_value_descriptions_schema() -> dict:
    return get_dict_from_json_file(current_app.config.get("VALUE_DESCRIPTIONS_SCHEMA"))
