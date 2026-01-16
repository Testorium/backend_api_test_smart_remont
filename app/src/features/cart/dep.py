from typing import Annotated

from fastapi import Depends
from src.database import SessionDep

from .repo import CartItemRepository, CartRepository
from .service import CartItemService, CartService


def get_cart_service(session: SessionDep) -> CartService:
    repo = CartRepository(session=session)
    return CartService(repo=repo)


CartServiceDep = Annotated[CartService, Depends(get_cart_service)]


def get_cart_item_service(session: SessionDep) -> CartItemService:
    repo = CartItemRepository(session=session)
    return CartItemService(repo=repo)


CartItemServiceDep = Annotated[CartItemService, Depends(get_cart_item_service)]
