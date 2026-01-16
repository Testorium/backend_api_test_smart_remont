from uuid import UUID

from pydantic import BaseModel


class UUIDPrimaryKeySchema(BaseModel):
    id: UUID
