from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, declarative_mixin, mapped_column
from src.model.types import DateTimeUTC


@declarative_mixin
class VerificationColumns:
    """Verification / approval state."""

    is_verified: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
        index=True,
        sort_order=3400,
    )

    verified_at: Mapped[datetime | None] = mapped_column(
        DateTimeUTC(timezone=True),
        nullable=True,
        sort_order=3401,
    )

    def verify(self) -> None:
        self.is_verified = True
        self.verified_at = datetime.now(timezone.utc)

    def unverify(self) -> None:
        self.is_verified = False
        self.verified_at = None
