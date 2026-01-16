from functools import cached_property
from typing import List, cast

from src.model import Base
from src.repo.base import BaseRepository
from src.schema import BaseSchema


class BaseService[
    CreateSchemaT: BaseSchema,
    # UpdateSchemaT: BaseSchema,
    RepositoryT: BaseRepository[ModelT],
    ModelT: Base,
]:
    def __init__(
        self,
        repo: RepositoryT,
    ) -> None:
        self.repo = repo

    @cached_property
    def model(self) -> type[ModelT]:
        return cast("type[ModelT]", self.repo.model)

    async def add(self, data: CreateSchemaT) -> ModelT:
        instance = self.model(**data.model_dump())
        return await self.repo.add(
            instance,
            auto_commit=True,
        )

    async def list(self) -> List[ModelT]:
        return await self.repo.list()
