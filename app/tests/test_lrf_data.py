from app.common.db_utils import create_sqlalchemy_engine


def test_lrf_data_exists():
    engine = create_sqlalchemy_engine()
    with engine.connect() as con:
        lrf_data_count = con.execute("SELECT COUNT(*) FROM lrf_data").scalar()
        assert lrf_data_count == 38362

        column_names = con.execute(
            "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='lrf_data'"
        ).fetchall()
        assert len(column_names) == 6
