from datetime import datetime, timezone

from pydantic import BaseModel, field_validator


class AuditColumnsSchema(BaseModel):
    created_at: datetime
    updated_at: datetime

    @field_validator("created_at", "updated_at")
    @classmethod
    def ensure_tzinfo(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v
