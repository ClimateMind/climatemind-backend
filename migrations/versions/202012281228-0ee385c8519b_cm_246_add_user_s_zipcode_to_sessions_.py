"""CM-246 add user's zipcode to Sessions table, column: postal_code

Revision ID: 0ee385c8519b
Revises: 0ad601cccfdd
Create Date: 2020-12-28 12:28:33.229769

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0ee385c8519b"
down_revision = "0ad601cccfdd"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("sessions", sa.Column("postal_code", sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("sessions", "postal_code")
    # ### end Alembic commands ###
