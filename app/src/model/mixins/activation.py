from sqlalchemy.orm import Mapped, declarative_mixin, mapped_column


@declarative_mixin
class ActivationColumns:
    """Operational availability."""

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
        index=True,
        sort_order=3300,
    )

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False
