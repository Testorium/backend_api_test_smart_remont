from uuid import UUID

from src.schema import BaseSchema
from src.schema.mixins import AuditColumnsSchema, INTPrimaryKeySchema


class PostBaseSchema(BaseSchema):
    name: str
    user_id: UUID


class PostCreateSchema(PostBaseSchema): ...


class PostReadSchema(
    INTPrimaryKeySchema,
    PostBaseSchema,
    AuditColumnsSchema,
): ...
