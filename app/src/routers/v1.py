from fastapi import APIRouter
from src.features.post.router import router as post_router
from src.features.user.router import router as user_router

from .prefix_config import api_prefix_config

v1_router = APIRouter(prefix=api_prefix_config.v1.prefix)


v1_router.include_router(user_router)
v1_router.include_router(post_router)
