from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from src.routers import main_router

from .database import db_manager


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    db_manager.initialize()
    yield
    await db_manager.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(main_router)
