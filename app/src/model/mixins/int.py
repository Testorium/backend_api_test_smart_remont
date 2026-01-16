from sqlalchemy.orm import Mapped, declarative_mixin, mapped_column


@declarative_mixin
class INTPrimaryKey:
    """INT Primary Key Field Mixin."""

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, sort_order=-100
    )
    """INT Primary key column."""
