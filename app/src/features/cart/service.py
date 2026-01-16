from uuid import UUID

from sqlalchemy.orm import selectinload
from src.features.product.schema import ProductRead
from src.service import BaseService

from .model import Cart, CartItem
from .repo import CartItemRepository, CartRepository
from .schema import CartCreate, CartItemCreate, CartItemRead, CartRead


class CartService(
    BaseService[
        CartCreate,
        CartRepository,
        Cart,
    ]
):
    async def add(self, session_id: str) -> Cart:
        instance = self.model(session_id=session_id)
        return await self.repo.add(
            instance,
            auto_commit=True,
        )

    async def get_one(self, **kwargs) -> Cart:
        load_options = [selectinload(Cart.items).selectinload(CartItem.product)]
        return await self.repo.get_one(load_options=load_options, **kwargs)

    async def get_one_or_none(self, **kwargs) -> Cart:
        return await self.repo.get_one_or_none(**kwargs)

    async def get_cart_items(self, *, session_id: str) -> CartRead:
        cart = await self.get_one(session_id=session_id)
        total_price = sum(item.product.price * item.quantity for item in cart.items)

        return CartRead(
            id=cart.id,
            session_id=cart.session_id,
            total_price=float(total_price),
            items=[
                CartItemRead(
                    id=item.id,
                    quantity=item.quantity,
                    product=ProductRead.model_validate(item.product),
                )
                for item in cart.items
            ],
        )


class CartItemService(
    BaseService[
        CartItemCreate,
        CartItemRepository,
        CartItem,
    ]
):
    async def add(self, data: CartItemCreate, cart_id: UUID) -> CartItem:
        instance = self.model(**data.model_dump(), cart_id=cart_id)
        return await self.repo.add(
            instance,
            auto_commit=True,
        )

    async def update(self, *, item: CartItem) -> CartItem:
        return await self.repo.update(item, auto_commit=True)

    async def delete_item_by_id(self, *, item_id: UUID) -> None:
        item = await self.repo.get_one(id=item_id)
        await self.repo.delete(item, auto_commit=True)
