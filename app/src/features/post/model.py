from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from src.model import Base
from src.model.mixins import AuditColumns, INTPrimaryKey


class Post(Base, INTPrimaryKey, AuditColumns):
    name: Mapped[str] = mapped_column(String(50))

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
