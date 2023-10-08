"""499 explicit ondelete

Revision ID: ec4000ea90cb
Revises: 7d5d345fee36
Create Date: 2023-10-03 11:47:59.542592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ec4000ea90cb"
down_revision = "7d5d345fee36"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint(
        "fk_conversations__sender_user_uuid__users", "conversations", type_="foreignkey"
    )
    op.create_foreign_key(
        None,
        "conversations",
        "users",
        ["sender_user_uuid"],
        ["user_uuid"],
        ondelete="SET NULL",
    )

    op.drop_constraint(
        "fk_password_reset_links__user_uuid__users",
        "password_reset_links",
        type_="foreignkey",
    )
    op.create_foreign_key(
        None,
        "password_reset_links",
        "users",
        ["user_uuid"],
        ["user_uuid"],
        ondelete="cascade",
    )

    op.drop_constraint("fk_sessions__user_uuid__users", "sessions", type_="foreignkey")
    op.create_foreign_key(
        None, "sessions", "users", ["user_uuid"], ["user_uuid"], ondelete="SET NULL"
    )


def downgrade():
    op.drop_constraint(
        "fk_conversations__sender_user_uuid__users", "conversations", type_="foreignkey"
    )
    op.create_foreign_key(
        None, "conversations", "users", ["sender_user_uuid"], ["user_uuid"]
    )

    op.drop_constraint(
        "fk_password_reset_links__user_uuid__users",
        "password_reset_links",
        type_="foreignkey",
    )
    op.create_foreign_key(
        None, "password_reset_links", "users", ["user_uuid"], ["user_uuid"]
    )

    op.drop_constraint("fk_sessions__user_uuid__users", "sessions", type_="foreignkey")
    op.create_foreign_key(None, "sessions", "users", ["user_uuid"], ["user_uuid"])
