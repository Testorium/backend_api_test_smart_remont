from typing import TYPE_CHECKING, AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .config import db_config

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession


class AsyncDatabaseManager:
    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 10,
        max_overflow: int = 50,
    ):
        self.engine: "AsyncEngine" = create_async_engine(
            url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )

        self.session_factory: async_sessionmaker["AsyncSession"] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def get_session(self) -> AsyncGenerator["AsyncSession", None]:
        async with self.session_factory() as session:
            yield session


db_manager = AsyncDatabaseManager(
    url=db_config.dns,
    echo=db_config.echo,
    echo_pool=db_config.echo_pool,
    pool_size=db_config.pool_size,
    max_overflow=db_config.max_overflow,
)
