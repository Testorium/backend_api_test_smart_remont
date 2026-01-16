from typing import TYPE_CHECKING, List
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.model import Base
from src.model.mixins import UUIDPrimaryKey

if TYPE_CHECKING:
    from src.features.product.model import Product


class Cart(Base, UUIDPrimaryKey):
    session_id: Mapped[str] = mapped_column(String(50), unique=True)
    items: Mapped[List["CartItem"]] = relationship(
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class CartItem(Base, UUIDPrimaryKey):
    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id"))
    cart_id: Mapped[UUID] = mapped_column(ForeignKey("carts.id"))
    quantity: Mapped[int]

    product: Mapped["Product"] = relationship()
