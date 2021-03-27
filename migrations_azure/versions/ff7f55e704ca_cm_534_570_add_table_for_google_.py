"""CM-534-570 add table for google analytics data

Revision ID: ff7f55e704ca
Revises: 73360b3341d2
Create Date: 2021-03-08 06:58:41.279460

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = "ff7f55e704ca"
down_revision = "73360b3341d2"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "analytics_data",
        sa.Column("analytics_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("category", sa.String(length=50), nullable=True),
        sa.Column("action", sa.String(length=50), nullable=True),
        sa.Column("label", sa.String(length=50), nullable=True),
        sa.Column("session_uuid", mssql.UNIQUEIDENTIFIER(), nullable=True),
        sa.Column("event_timestamp", sa.DateTime(), nullable=True),
        sa.Column("value", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("analytics_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("analytics_data")
    # ### end Alembic commands ###
