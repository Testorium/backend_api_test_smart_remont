import uuid

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, declarative_mixin, mapped_column


@declarative_mixin
class UUIDPrimaryKey:
    """UUID Primary Key Field Mixin."""

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, sort_order=-100
    )
    """UUID Primary key column."""
