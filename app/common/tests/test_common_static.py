import os

from app.common.static import get_dict_from_json_file


def test_get_dict_from_json_file():
    file_name = os.path.join(os.getcwd(), "app/common/tests/data/static.json")
    data_from_file = get_dict_from_json_file(file_name)
    assert data_from_file == {"test": 123}
