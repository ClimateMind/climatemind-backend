import pytest

from app.common.db_utils import create_sqlalchemy_engine


@pytest.mark.lrf_data
def test_lrf_data_exists():
    engine = create_sqlalchemy_engine()
    with engine.connect() as con:
        column_tuples = con.execute(
            "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='lrf_data'"
        ).fetchall()
        column_names = set([column_tuple[0] for column_tuple in column_tuples])
        expected_column_names = set(
            [
                "postal_code",
                "http://webprotege.stanford.edu/R9vkBr0EApzeMGfa0rJGo9G",
                "http://webprotege.stanford.edu/RDudF9SBo28CKqKpRN9poYL",
                "http://webprotege.stanford.edu/RJAL6Zu9F3EHB35HCs3cYD",
                "http://webprotege.stanford.edu/RLc1ySxaRs4HWkW4m5w2Me",
                "http://webprotege.stanford.edu/RcIHdxpjQwjr8EG8yMhEYV",
            ]
        )
        assert column_names == expected_column_names
