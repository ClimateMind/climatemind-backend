import pytest

from app.post_code.store_post_code import is_post_code_valid


@pytest.mark.skip("To be fixed")
@pytest.mark.parametrize(
    "raw_post_code,valid_post_code",
    [
        ("osidfjsidfj", False),
        ("12321", True),
        ("ijsdf12312 isdfo", False),
        ("siofdj 12312 i", False),
        ("213 12312 1", False),
        ("12323 12312 1", False),
    ],
)
def test_check_post_code(
    raw_post_code,
    valid_post_code,
):
    assert is_post_code_valid(raw_post_code) == valid_post_code
