"""This migration created manually to populate local db with a lrf_data
"""
import os

from alembic import op


# revision identifiers, used by Alembic.

revision = "9999db04b3ae"
down_revision = "3386db04b3ae"
branch_labels = None
depends_on = None


def upgrade():
    if os.environ.get("IS_LOCAL"):
        from migrations.scripts.lrf.add_lrf_table import add_lrf_data

        add_lrf_data()


def downgrade():
    op.drop_table("lrf_data")
