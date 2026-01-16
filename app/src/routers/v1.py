from fastapi import APIRouter
from src.features.cart.router import router as cart_router
from src.features.product.router import router as product_router

from .prefix_config import api_prefix_config

v1_router = APIRouter(prefix=api_prefix_config.v1.prefix)


v1_router.include_router(product_router)
v1_router.include_router(cart_router)
