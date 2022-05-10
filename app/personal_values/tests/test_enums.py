from app.personal_values.enums import PersonalValue


def test_personal_values_sorting():
    real_order_ids = list(PersonalValue)
    sorted_order_ids = sorted(PersonalValue)
    assert real_order_ids != sorted_order_ids, "Sorting by values (IDs) is wrong."

    keys_order = [v.key for v in PersonalValue]
    sorted_keys_order = sorted([v.key for v in PersonalValue])
    assert keys_order == sorted_keys_order, "Enum should by sorted by key"

    assert sorted_keys_order == PersonalValue.get_all_keys(), "Helper method order"
