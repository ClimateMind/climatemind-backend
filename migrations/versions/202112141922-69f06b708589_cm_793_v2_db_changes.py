"""CM-793 V2 DB changes

Revision ID: 69f06b708589
Revises: d699bd7eb7e9
Create Date: 2021-12-14 19:22:07.245900

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = "69f06b708589"
down_revision = "d699bd7eb7e9"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "alignment_feed",
        sa.Column("alignment_feed_uuid", mssql.UNIQUEIDENTIFIER(), nullable=False),
        sa.Column("aligned_effect_1_iri", sa.String(length=255), nullable=True),
        sa.Column("aligned_effect_2_iri", sa.String(length=255), nullable=True),
        sa.Column("aligned_effect_3_iri", sa.String(length=255), nullable=True),
        sa.Column("aligned_solution_1_iri", sa.String(length=255), nullable=True),
        sa.Column("aligned_solution_2_iri", sa.String(length=255), nullable=True),
        sa.Column("aligned_solution_3_iri", sa.String(length=255), nullable=True),
        sa.Column("aligned_solution_4_iri", sa.String(length=255), nullable=True),
        sa.Column("aligned_solution_5_iri", sa.String(length=255), nullable=True),
        sa.Column("aligned_solution_6_iri", sa.String(length=255), nullable=True),
        sa.Column("aligned_solution_7_iri", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("alignment_feed_uuid"),
    )
    op.create_table(
        "alignment_scores",
        sa.Column("alignment_scores_uuid", mssql.UNIQUEIDENTIFIER(), nullable=False),
        sa.Column("overall_similarity_score", sa.Float(), nullable=True),
        sa.Column("top_match_percent", sa.Float(), nullable=True),
        sa.Column("top_match_value", sa.String(length=255), nullable=True),
        sa.Column("security_alignment", sa.Float(), nullable=True),
        sa.Column("conformity_alignment", sa.Float(), nullable=True),
        sa.Column("benevolence_alignment", sa.Float(), nullable=True),
        sa.Column("tradition_alignment", sa.Float(), nullable=True),
        sa.Column("universalism_alignment", sa.Float(), nullable=True),
        sa.Column("self_direction_alignment", sa.Float(), nullable=True),
        sa.Column("stimulation_alignment", sa.Float(), nullable=True),
        sa.Column("hedonism_alignment", sa.Float(), nullable=True),
        sa.Column("achievement_alignment", sa.Float(), nullable=True),
        sa.Column("power_alignment", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("alignment_scores_uuid"),
    )
    op.create_table(
        "effect_choice",
        sa.Column("effect_choice_uuid", mssql.UNIQUEIDENTIFIER(), nullable=False),
        sa.Column("effect_choice_1_iri", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("effect_choice_uuid"),
    )
    op.create_table(
        "solution_choice",
        sa.Column("solution_choice_uuid", mssql.UNIQUEIDENTIFIER(), nullable=False),
        sa.Column("solution_choice_1_iri", sa.String(length=255), nullable=True),
        sa.Column("solution_choice_2_iri", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("solution_choice_uuid"),
    )
    op.create_table(
        "user_b_analytics_data",
        sa.Column("event_log_uuid", mssql.UNIQUEIDENTIFIER(), nullable=False),
        sa.Column("conversation_uuid", mssql.UNIQUEIDENTIFIER(), nullable=True),
        sa.Column("event_type", sa.String(length=255), nullable=True),
        sa.Column("event_value", sa.String(length=255), nullable=True),
        sa.Column("event_timestamp", sa.DateTime(), nullable=True),
        sa.Column("event_value_type", sa.String(length=255), nullable=True),
        sa.Column("session_uuid", mssql.UNIQUEIDENTIFIER(), nullable=True),
        sa.ForeignKeyConstraint(
            ["conversation_uuid"],
            ["conversations.conversation_uuid"],
        ),
        sa.ForeignKeyConstraint(
            ["session_uuid"],
            ["sessions.session_uuid"],
        ),
        sa.PrimaryKeyConstraint("event_log_uuid"),
    )
    op.create_table(
        "user_b_journey",
        sa.Column("conversation_uuid", mssql.UNIQUEIDENTIFIER(), nullable=False),
        sa.Column("quiz_uuid", mssql.UNIQUEIDENTIFIER(), nullable=True),
        sa.Column("alignment_scores_uuid", mssql.UNIQUEIDENTIFIER(), nullable=True),
        sa.Column("alignment_feed_uuid", mssql.UNIQUEIDENTIFIER(), nullable=True),
        sa.Column("effect_choice_uuid", mssql.UNIQUEIDENTIFIER(), nullable=True),
        sa.Column("solution_choice_uuid", mssql.UNIQUEIDENTIFIER(), nullable=True),
        sa.Column("consent", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(
            ["alignment_feed_uuid"],
            ["alignment_feed.alignment_feed_uuid"],
        ),
        sa.ForeignKeyConstraint(
            ["alignment_scores_uuid"],
            ["alignment_scores.alignment_scores_uuid"],
        ),
        sa.ForeignKeyConstraint(
            ["conversation_uuid"],
            ["conversations.conversation_uuid"],
        ),
        sa.ForeignKeyConstraint(
            ["effect_choice_uuid"],
            ["effect_choice.effect_choice_uuid"],
        ),
        sa.ForeignKeyConstraint(
            ["quiz_uuid"],
            ["scores.quiz_uuid"],
        ),
        sa.ForeignKeyConstraint(
            ["solution_choice_uuid"],
            ["solution_choice.solution_choice_uuid"],
        ),
        sa.PrimaryKeyConstraint("conversation_uuid"),
    )
    op.add_column(
        "conversations", sa.Column("user_b_share_consent", sa.Boolean(), nullable=True)
    )
    op.drop_constraint(
        "fk_conversations__receiver_session_uuid__sessions",
        "conversations",
        type_="foreignkey",
    )
    op.drop_column("conversations", "receiver_session_uuid")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "conversations",
        sa.Column(
            "receiver_session_uuid",
            mssql.UNIQUEIDENTIFIER(),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.create_foreign_key(
        "fk_conversations__receiver_session_uuid__sessions",
        "conversations",
        "sessions",
        ["receiver_session_uuid"],
        ["session_uuid"],
    )
    op.drop_column("conversations", "user_b_share_consent")
    op.drop_table("user_b_journey")
    op.drop_table("user_b_analytics_data")
    op.drop_table("solution_choice")
    op.drop_table("effect_choice")
    op.drop_table("alignment_scores")
    op.drop_table("alignment_feed")
    # ### end Alembic commands ###
