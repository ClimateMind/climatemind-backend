from json import load


def get_dict_from_json_file(json_file_name: str) -> dict:
    with open(json_file_name) as json_file:
        data = load(json_file)
    return data
