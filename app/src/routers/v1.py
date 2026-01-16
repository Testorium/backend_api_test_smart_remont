from fastapi import APIRouter

from .prefix_config import api_prefix_config

v1_router = APIRouter(prefix=api_prefix_config.v1.prefix)
