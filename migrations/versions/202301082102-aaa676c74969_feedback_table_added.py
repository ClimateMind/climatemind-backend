"""feedback table added

Revision ID: aaa676c74969
Revises: 2b11a0ca6ddc
Create Date: 2023-01-08 21:02:22.979248

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = "aaa676c74969"
down_revision = "2b11a0ca6ddc"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "feedback",
        sa.Column("feedback_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("session_uuid", mssql.UNIQUEIDENTIFIER(), nullable=False),
        sa.Column("feedback_created_timestamp", sa.DateTime(), nullable=False),
        sa.Column("text", sa.String(length=2048), nullable=False),
        sa.ForeignKeyConstraint(
            ["session_uuid"],
            ["sessions.session_uuid"],
            name=op.f("fk_feedback__session_uuid__sessions"),
        ),
        sa.PrimaryKeyConstraint("feedback_id", name=op.f("pk_feedback")),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("feedback")
    # ### end Alembic commands ###
