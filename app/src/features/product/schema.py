from typing import Optional
from uuid import UUID

from src.schema import BaseSchema


class ProductCreate(BaseSchema):
    name: str
    description: Optional[str] = None
    price: float

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
    price: Optional[float] = None

    image: Optional[str] = None
    category: Optional[str] = None
