import os
from json import load
from flask import jsonify

def get_value_descriptions_map():
    """Get a name->description dict for all values."""
    try:
        file = os.path.join(
            os.getcwd(), "app/personal_values/static", "value_descriptions.json"
        )
        with open(file) as f:
            data = load(f)
    except FileNotFoundError:
        return jsonify({"error": "Value descriptions file not found"}), 404
    return data
