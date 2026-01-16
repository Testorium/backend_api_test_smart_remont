from src.schema import BaseSchema
from src.schema.mixins import AuditColumnsSchema, UUIDPrimaryKeySchema


class UserBaseSchema(BaseSchema):
    first_name: str
    last_name: str


class UserCreateSchema(UserBaseSchema): ...


class UserReadSchema(
    AuditColumnsSchema,
    UserBaseSchema,
    UUIDPrimaryKeySchema,
): ...
