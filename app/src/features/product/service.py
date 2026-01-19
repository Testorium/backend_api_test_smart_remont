import math
from typing import List, Literal, Optional
from uuid import UUID

from sqlalchemy import ColumnElement, asc, desc, or_
from src.schema.pagination import PageMeta, PaginatedResponse
from src.service import BaseService

from .model import Product
from .repo import ProductRepository
from .schema import ProductCreate, ProductRead


class ProductService(
    BaseService[
        ProductCreate,
        ProductRepository,
        Product,
    ]
):
    # Я использую собственный FastAPI starterpack с базовым репозиторием и базовым сервисом,
    # но на данный момент он ещё не завершён, поэтому часть методов реализована здесь,
    # а не в BaseService. (чисто для данного ТЗ)

    # async def get_one_by_id(self, product_id: UUID) -> Product:
    #     return await self.repo.get_one(id=product_id)

    async def list_products(
        self,
        *,
        page: int,
        page_size: int,
        search: Optional[str] = None,
        category: Optional[str] = None,
        price_from: Optional[float] = None,
        price_to: Optional[float] = None,
        sort_by: Optional[Literal["price", "name"]] = None,
        sort_order: Literal["asc", "desc"] = "asc",
    ) -> PaginatedResponse[ProductRead]:
        conditions = self._build_product_conditions(
            search=search,
            category=category,
            price_from=price_from,
            price_to=price_to,
        )

        total = await self.repo.count(conditions)

        limit = page_size
        offset = (page - 1) * page_size

        order_by = None
        if sort_by:
            column = self.repo._get_instrumented_attr(self.model, sort_by)
            order_by = [asc(column) if sort_order == "asc" else desc(column)]

        items = await self.repo.list(
            limit=limit,
            offset=offset,
            conditions=conditions,
            order_by=order_by,
        )

        total_pages = (total + page_size - 1) // page_size

        return PaginatedResponse(
            items=items,
            meta=PageMeta(
                total=total,
                page=page,
                page_size=page_size,
                total_pages=total_pages,
            ),
        )

    @staticmethod
    def _build_product_conditions(
        *,
        search: Optional[str] = None,
        category: Optional[str] = None,
        price_from: Optional[float] = None,
        price_to: Optional[float] = None,
    ) -> List[ColumnElement[bool]]:
        conditions: List[ColumnElement[bool]] = []

        if search:
            conditions.append(
                or_(
                    Product.name.ilike(f"%{search}%"),
                    Product.description.ilike(f"%{search}%"),
                )
            )

        if category:
            conditions.append(Product.category.ilike(f'%{category}%'))

        if price_from:
            conditions.append(Product.price >= price_from)

        if price_to:
            conditions.append(Product.price <= price_to)

        return conditions
