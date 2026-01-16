"""create_posts

Revision ID: a82ade2e14b5
Revises: 2264d670125d
Create Date: 2025-12-30 13:41:34.249926

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from src.model.types import DateTimeUTC

revision: str = "a82ade2e14b5"
down_revision: Union[str, Sequence[str], None] = "2264d670125d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            DateTimeUTC(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            DateTimeUTC(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_posts_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_posts")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("posts")
