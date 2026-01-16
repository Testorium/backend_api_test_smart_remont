from typing import Optional
from uuid import UUID

from pydantic import PositiveFloat
from src.schema import BaseSchema


class ProductCreate(BaseSchema):
    name: str
    description: Optional[str] = None
    price: PositiveFloat

    category: str


class ProductRead(BaseSchema):
    id: UUID
    name: str
    description: Optional[str] = None
    price: float

    image: Optional[str] = None
    category: str


class ProductUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[PositiveFloat] = None

    image: Optional[str] = None
    category: Optional[str] = None
