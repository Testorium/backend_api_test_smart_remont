"""create_product_and_card

Revision ID: 6a08fb54906f
Revises:
Create Date: 2026-01-16 19:06:04.567508

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from src.model.types import DateTimeUTC

revision: str = "6a08fb54906f"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "carts",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("session_id", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_carts")),
        sa.UniqueConstraint("session_id", name=op.f("uq_carts_session_id")),
    )
    op.create_table(
        "products",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.TEXT(), nullable=True),
        sa.Column("price", sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column("image", sa.String(), nullable=True),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("created_at", DateTimeUTC(timezone=True), nullable=False),
        sa.Column("updated_at", DateTimeUTC(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_products")),
        sa.UniqueConstraint("name", name=op.f("uq_products_name")),
    )
    op.create_index(
        op.f("ix_products_category"), "products", ["category"], unique=False
    )
    op.create_table(
        "cart_items",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("product_id", sa.UUID(), nullable=False),
        sa.Column("cart_id", sa.UUID(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["cart_id"], ["carts.id"], name=op.f("fk_cart_items_cart_id_carts")
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
            name=op.f("fk_cart_items_product_id_products"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_cart_items")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("cart_items")
    op.drop_index(op.f("ix_products_category"), table_name="products")
    op.drop_table("products")
    op.drop_table("carts")
