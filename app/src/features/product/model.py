from sqlalchemy import DECIMAL
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column
from src.model import Base
from src.model.mixins import AuditColumns, UUIDPrimaryKey


class Product(Base, UUIDPrimaryKey, AuditColumns):
    name: Mapped[str] = mapped_column(unique=True)  # чисто для этого случая
    description: Mapped[str] = mapped_column(TEXT, nullable=True)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))

    image: Mapped[str] = mapped_column(nullable=True)
    category: Mapped[str] = mapped_column(index=True)
