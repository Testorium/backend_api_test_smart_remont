from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import main_router

from .config import cors_config
from .database import db_manager
from .exception_handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    db_manager.initialize()
    yield
    await db_manager.dispose()


app = FastAPI(lifespan=lifespan, redirect_slashes=False)
app.include_router(main_router)
register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_config.allow_origins,
    allow_credentials=cors_config.allow_credentials,
    allow_methods=cors_config.allow_methods,
    allow_headers=cors_config.allow_headers,
)
