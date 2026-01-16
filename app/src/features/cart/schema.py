from typing import List
from uuid import UUID

from pydantic import PositiveInt
from src.features.product.schema import ProductRead
from src.schema import BaseSchema


class CartCreate(BaseSchema): ...


class CartItemCreate(BaseSchema):
    product_id: UUID
    quantity: int


class CartItemUpdate(BaseSchema):
    quantity: int = PositiveInt


class CartItemRead(BaseSchema):
    id: UUID
    quantity: int
    product: ProductRead


class CartRead(BaseSchema):
    id: UUID
    session_id: str
    total_price: float
    items: List[CartItemRead]
