from typing import List, Literal, Optional
from uuid import UUID

from fastapi import APIRouter, Query
from src.routers import api_prefix_config
from src.schema.pagination import PaginatedResponse

from .dep import ProductServiceDep
from .schema import ProductCreate, ProductRead

router = APIRouter(prefix=api_prefix_config.v1.products, tags=["Products"])


@router.get("/", response_model=PaginatedResponse[ProductRead])
async def list_all_products(
    service: ProductServiceDep,
    category: Optional[str] = Query(None),
    price_from: Optional[float] = Query(None, ge=0),
    price_to: Optional[float] = Query(None, ge=0),
    search: Optional[str] = Query(None),
    sort_by: Optional[Literal["price", "name"]] = None,
    sort_order: Literal["asc", "desc"] = "asc",
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
):
    return await service.list_products(
        page=page,
        page_size=page_size,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        category=category,
        price_from=price_from,
        price_to=price_to,
    )


@router.post("/", response_model=ProductRead)
async def create_new_product(
    data: ProductCreate,
    service: ProductServiceDep,
):
    return await service.add(data)


@router.post("/bulk", response_model=List[ProductRead])
async def bulk_create_new_product(
    data: List[ProductCreate],
    service: ProductServiceDep,
):
    products = []
    for product_data in data:
        product = await service.add(product_data)
        products.append(product)

    return products


@router.get("/{product_id}", response_model=ProductRead)
async def get_product_by_id(
    product_id: UUID,
    service: ProductServiceDep,
):
    return await service.get_one_by_id(id=product_id)
