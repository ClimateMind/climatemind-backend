"""put lrf table back

Revision ID: d10c6bfdd9aa
Revises: 65c5753b57e0
Create Date: 2021-01-11 10:31:39.441091

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = "d10c6bfdd9aa"
down_revision = "65c5753b57e0"
branch_labels = None
depends_on = None


def upgrade():
    # NOTE: commented due to usage outside alembic migration cycle
    # op.drop_index("ix_lrf_data_postal_code", table_name="lrf_data")
    # op.drop_table("lrf_data")
    pass


def downgrade():
    # NOTE: commented due to usage outside alembic migration cycle
    # op.create_table(
    #     "lrf_data",
    #     sa.Column("postal_code", sa.BIGINT(), autoincrement=False, nullable=True),
    #     sa.Column(
    #         "http://webprotege.stanford.edu/R9vkBr0EApzeMGfa0rJGo9G",
    #         mssql.BIT(),
    #         autoincrement=False,
    #         nullable=True,
    #     ),
    #     sa.Column(
    #         "http://webprotege.stanford.edu/RJAL6Zu9F3EHB35HCs3cYD",
    #         mssql.BIT(),
    #         autoincrement=False,
    #         nullable=True,
    #     ),
    #     sa.Column(
    #         "http://webprotege.stanford.edu/RcIHdxpjQwjr8EG8yMhEYV",
    #         mssql.BIT(),
    #         autoincrement=False,
    #         nullable=True,
    #     ),
    #     sa.Column(
    #         "http://webprotege.stanford.edu/RDudF9SBo28CKqKpRN9poYL",
    #         mssql.BIT(),
    #         autoincrement=False,
    #         nullable=True,
    #     ),
    #     sa.Column(
    #         "http://webprotege.stanford.edu/RLc1ySxaRs4HWkW4m5w2Me",
    #         mssql.BIT(),
    #         autoincrement=False,
    #         nullable=True,
    #     ),
    # )
    # op.create_index(
    #     "ix_lrf_data_postal_code", "lrf_data", ["postal_code"], unique=False
    # )
    pass
