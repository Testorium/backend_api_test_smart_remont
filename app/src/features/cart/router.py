from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Header, HTTPException
from fastapi import status as status_codes
from src.features.product.dep import ProductServiceDep
from src.routers import api_prefix_config

from .dep import CartItemServiceDep, CartServiceDep
from .schema import CartItemCreate, CartItemUpdate, CartRead

router = APIRouter(prefix=api_prefix_config.v1.carts, tags=["Carts"])


@router.post("/", status_code=status_codes.HTTP_201_CREATED)
async def add_item_to_cart(
    data: CartItemCreate,
    x_session_id: Annotated[str, Header()],
    cart_service: CartServiceDep,
    cart_item_service: CartItemServiceDep,
    product_service: ProductServiceDep,
):
    product = await product_service.get_one_by_id(id=data.product_id)
    data.product_id = product.id

    cart = await cart_service.get_one_or_none(session_id=x_session_id)

    if not cart:
        cart = await cart_service.add(session_id=x_session_id)

    await cart_item_service.add(data=data, cart_id=cart.id)


@router.get("/", response_model=CartRead)
async def get_cart_items(
    x_session_id: Annotated[str, Header()],
    cart_service: CartServiceDep,
):
    cart = await cart_service.get_one_or_none(session_id=x_session_id)

    if not cart:
        cart = await cart_service.add(session_id=x_session_id)

    return await cart_service.get_cart_items(session_id=x_session_id)


@router.patch("/{cart_item_id}/", status_code=status_codes.HTTP_200_OK)
async def update_cart_item(
    x_session_id: Annotated[str, Header()],
    cart_item_id: UUID,
    data: CartItemUpdate,
    cart_service: CartServiceDep,
    cart_item_service: CartItemServiceDep,
):
    cart = await cart_service.get_one(session_id=x_session_id)
    cart_item = await cart_item_service.get_one_by_id(id=cart_item_id)

    cart_item_ids = [ci.id for ci in cart.items]

    if cart_item.id not in cart_item_ids:
        raise HTTPException(
            status_code=status_codes.HTTP_400_BAD_REQUEST,
            detail="It is not your item! Don't touch it!",
        )

    cart_item.quantity = data.quantity
    await cart_item_service.update(item=cart_item)


@router.delete("/{cart_item_id}/", status_code=status_codes.HTTP_204_NO_CONTENT)
async def delete_cart_item(
    x_session_id: Annotated[str, Header()],
    cart_item_id: UUID,
    cart_service: CartServiceDep,
    cart_item_service: CartItemServiceDep,
):
    cart = await cart_service.get_one(session_id=x_session_id)
    cart_item = await cart_item_service.get_one_by_id(id=cart_item_id)

    cart_item_ids = [ci.id for ci in cart.items]

    if cart_item.id not in cart_item_ids:
        raise HTTPException(
            status_code=status_codes.HTTP_400_BAD_REQUEST,
            detail="It is not your item! Don't touch it!",
        )

    await cart_item_service.delete_item_by_id(item_id=cart_item.id)
