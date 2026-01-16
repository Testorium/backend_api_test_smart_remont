from pydantic import BaseModel, PositiveInt


class INTPrimaryKeySchema(BaseModel):
    id: PositiveInt
