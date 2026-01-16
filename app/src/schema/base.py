from humps import camelize
from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict


class BaseSchema(_BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=camelize,
        validate_by_alias=True,
        validate_by_name=True,
    )
