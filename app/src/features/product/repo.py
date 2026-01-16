from src.repo import BaseRepository

from .constant import PRODUCT_ERROR_MESSAGES
from .model import Product


class ProductRepository(BaseRepository[Product]):
    model = Product
    order_by = [Product.created_at]
    error_messages = PRODUCT_ERROR_MESSAGES
