from typing import Optional

from src.repo import BaseRepository
from src.repo.exceptions import ErrorMessages, wrap_sqlalchemy_exception

from .constant import CART_ERROR_MESSAGES, CART_ITEM_ERROR_MESSAGES
from .model import Cart, CartItem


class CartRepository(BaseRepository[Cart]):
    model = Cart
    error_messages = CART_ERROR_MESSAGES


class CartItemRepository(BaseRepository[CartItem]):
    model = CartItem
    error_messages = CART_ITEM_ERROR_MESSAGES

    async def delete(
        self,
        cart_item: CartItem,
        *,
        auto_commit: Optional[bool] = None,
        error_messages: Optional[ErrorMessages | None] = None,
    ) -> None:
        error_messages = self._get_error_messages(
            error_messages=error_messages,
            default_messages=self.error_messages,
        )

        with wrap_sqlalchemy_exception(error_messages=error_messages):
            await self.session.delete(cart_item)
            await self._flush_or_commit(auto_commit=auto_commit)
