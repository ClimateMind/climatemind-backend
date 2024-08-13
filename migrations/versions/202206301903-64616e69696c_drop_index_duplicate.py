"""drop index duplicate

Revision ID: 64616e69696c
Revises: f3cbcfe42467
Create Date: 2022-06-30 19:03:01.414667

"""

from alembic import op


# revision identifiers, used by Alembic.
revision = "64616e69696c"
down_revision = "f3cbcfe42467"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_index("ix_users__email", table_name="users")


def downgrade():
    # this query could fail since there's no `email` field anymore
    # op.create_index(None, "users", ["email"], unique=True)
    pass
