import mock

from datetime import datetime, timedelta

from freezegun import freeze_time

from app.factories import faker, PasswordResetLinkFactory
from app.models import AlignmentScores, Scores, PasswordResetLink
from app.personal_values.enums import PersonalValue


def test_alignment_score_fields_equals_to_personal_values():
    alignment_fields = [
        k.replace("_alignment", "")
        for k in AlignmentScores.__dict__.keys()
        if k.endswith("_alignment")
    ]

    assert set(alignment_fields) == set(
        PersonalValue.get_all_keys()
    ), "All AlignmentScores _alignment fields should be equal to PersonalValues"


def test_personal_values_in_scores_fields():
    for v in PersonalValue:
        assert hasattr(Scores, v.key), f"{v.key} field is missing in Scores class"


faked_now = faker.date_time()


@freeze_time(faked_now)
def test_password_reset_expired_property():
    more_that_expire = datetime.now() - timedelta(
        hours=PasswordResetLink.EXPIRE_HOURS_COUNT + 1
    )
    password_reset = PasswordResetLinkFactory(created=more_that_expire)
    assert password_reset.expired, "PasswordResetLink should be expired"

    less_that_expire = datetime.now() - timedelta(
        hours=PasswordResetLink.EXPIRE_HOURS_COUNT - 1
    )
    password_reset = PasswordResetLinkFactory(created=less_that_expire)
    assert not password_reset.expired, "PasswordResetLink should not be expired"


def test_password_reset_url_with_default_url():
    password_reset = PasswordResetLinkFactory()
    assert password_reset.reset_url.startswith("https://app.climatemind.org")


@mock.patch("app.models.current_app")
def test_password_reset_url_with_configured_base_frontend_url(m_current_app):
    m_current_app.config.get.side_effect = (
        lambda key: "https://fake-url.local" if key == "BASE_FRONTEND_URL" else None
    )

    password_reset = PasswordResetLinkFactory()
    assert password_reset.reset_url.startswith("https://fake-url.local")
