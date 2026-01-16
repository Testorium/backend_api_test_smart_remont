from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, declarative_mixin, mapped_column
from src.model.types import DateTimeUTC


@declarative_mixin
class SoftDeleteColumns:
    """Logical deletion (row still exists in DB)."""

    is_deleted: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
        sort_order=3100,
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTimeUTC(timezone=True),
        nullable=True,
        sort_order=3101,
    )

    def soft_delete(self) -> None:
        self.is_deleted = True
        self.deleted_at = datetime.now(timezone.utc)

    def restore(self) -> None:
        self.is_deleted = False
        self.deleted_at = None
