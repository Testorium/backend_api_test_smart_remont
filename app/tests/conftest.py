from typing import AsyncGenerator

import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import db_manager
from src.database.manager import AsyncDatabaseManager
from src.features.cart.model import Cart, CartItem
from src.features.product.model import Product
from src.main import app
from src.model.base import Base
from tests.config import test_db_config

test_db_manager = AsyncDatabaseManager(
    url=test_db_config.dns,
    echo=test_db_config.echo,
    echo_pool=test_db_config.echo_pool,
    pool_size=test_db_config.pool_size,
    max_overflow=test_db_config.max_overflow,
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    test_db_manager.initialize()

    async with test_db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    await test_db_manager.dispose()


@pytest_asyncio.fixture(scope="function")
async def async_client():
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async for session in test_db_manager.get_session():
            yield session

    app.dependency_overrides[db_manager.get_session] = override_get_db

    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
            follow_redirects=True,
        ) as client:
            yield client

    app.dependency_overrides.clear()
