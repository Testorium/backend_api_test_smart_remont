from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.model import AuditColumns, Base, UUIDPrimaryKey

if TYPE_CHECKING:
    from src.features.post.model import Post


class User(Base, UUIDPrimaryKey, AuditColumns):
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))

    posts: Mapped[List["Post"]] = relationship()
