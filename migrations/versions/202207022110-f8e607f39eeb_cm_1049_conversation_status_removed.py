"""CM-1049 conversation status removed

Revision ID: f8e607f39eeb
Revises: 64616e69696c
Create Date: 2022-07-02 21:10:22.075285

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f8e607f39eeb"
down_revision = "64616e69696c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("conversations", "conversation_status")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "conversations",
        sa.Column(
            "conversation_status", sa.INTEGER(), autoincrement=False, nullable=True
        ),
    )
    # ### end Alembic commands ###
