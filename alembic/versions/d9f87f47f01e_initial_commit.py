"""Initial commit

Revision ID: d9f87f47f01e
Revises: 
Create Date: 2024-07-17 12:52:02.783104

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d9f87f47f01e"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "movies",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("imdb_id", sa.String(length=255), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("type", sa.String(length=255), nullable=True),
        sa.Column("description", sa.String(length=100000), nullable=True),
        sa.Column("release_year", sa.Integer(), nullable=True),
        sa.Column("age_certification", sa.String(length=255), nullable=True),
        sa.Column("runtime", sa.Integer(), nullable=True),
        sa.Column("genres", sa.String(length=255), nullable=True),
        sa.Column("imdb_score", sa.Float(), nullable=True),
        sa.Column("emotions", sa.String(length=255), nullable=True),
        sa.Column("length", sa.String(length=255), nullable=True),
        sa.Column("platform", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("movies")
    # ### end Alembic commands ###
