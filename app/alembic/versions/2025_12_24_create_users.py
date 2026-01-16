"""create_users

Revision ID: 2264d670125d
Revises:
Create Date: 2025-12-24 15:19:45.122083

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from src.model.types import DateTimeUTC

revision: str = "2264d670125d"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("first_name", sa.String(length=50), nullable=False),
        sa.Column("last_name", sa.String(length=50), nullable=False),
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
