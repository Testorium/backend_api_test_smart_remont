from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, declarative_mixin, mapped_column
from src.model.types import DateTimeUTC


@declarative_mixin
class ArchiveColumns:
    """Archived but not deleted (historical)."""

    is_archived: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
        sort_order=3200,
    )

    archived_at: Mapped[datetime | None] = mapped_column(
        DateTimeUTC(timezone=True),
        nullable=True,
        sort_order=3201,
    )

    def archive(self) -> None:
        self.is_archived = True
        self.archived_at = datetime.now(timezone.utc)

    def unarchive(self) -> None:
        self.is_archived = False
        self.archived_at = None
