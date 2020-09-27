"""uuid

Revision ID: ec7aa9f08c41
Revises: 
Create Date: 2020-09-24 22:11:38.325027

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ec7aa9f08c41"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "iri",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("iri", sa.String(length=120), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("iri"),
    )
    op.create_table(
        "zip",
        sa.Column("zip", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("zip"),
    )
    op.create_table(
        "lrf",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("zip_id", sa.Integer(), nullable=True),
        sa.Column("iri_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["iri_id"],
            ["iri.id"],
        ),
        sa.ForeignKeyConstraint(
            ["zip_id"],
            ["zip.zip"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=True),
        sa.Column("email", sa.String(length=120), nullable=True),
        sa.Column("password_hash", sa.String(length=128), nullable=True),
        sa.Column("zip", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["zip"],
            ["zip.zip"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=True)
    op.create_table(
        "scores",
        sa.Column("session_id", sa.String(), nullable=False),
        sa.Column("security", sa.Float(), nullable=True),
        sa.Column("conformity", sa.Float(), nullable=True),
        sa.Column("benevolence", sa.Float(), nullable=True),
        sa.Column("tradition", sa.Float(), nullable=True),
        sa.Column("universalism", sa.Float(), nullable=True),
        sa.Column("self_direction", sa.Float(), nullable=True),
        sa.Column("stimulation", sa.Float(), nullable=True),
        sa.Column("hedonism", sa.Float(), nullable=True),
        sa.Column("achievement", sa.Float(), nullable=True),
        sa.Column("power", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("session_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("scores")
    op.drop_index(op.f("ix_user_username"), table_name="user")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
    op.drop_table("lrf")
    op.drop_table("zip")
    op.drop_table("iri")
    # ### end Alembic commands ###
