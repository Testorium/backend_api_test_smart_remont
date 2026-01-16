from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime
from sqlalchemy.engine import Dialect
from sqlalchemy.types import TypeDecorator

__all__ = ("DateTimeUTC",)


class DateTimeUTC(TypeDecorator[datetime]):
    """Timezone Aware DateTime.

    Ensure UTC is stored in the database and that TZ aware dates are returned for all dialects.
    """

    impl = DateTime(timezone=True)
    cache_ok = True

    @property
    def python_type(self) -> type[datetime]:
        return datetime

    def process_bind_param(
        self, value: Optional[datetime], dialect: Dialect
    ) -> Optional[datetime]:
        if value is None:
            return value
        if not value.tzinfo:
            msg = "tzinfo is required"
            raise TypeError(msg)
        return value.astimezone(timezone.utc)

    def process_result_value(
        self, value: Optional[datetime], dialect: Dialect
    ) -> Optional[datetime]:
        if value is None:
            return value
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value
