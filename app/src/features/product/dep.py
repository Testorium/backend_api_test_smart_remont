from typing import Annotated

from fastapi import Depends
from src.database import SessionDep

from .repo import ProductRepository
from .service import ProductService


def get_product_service(session: SessionDep) -> ProductService:
    repo = ProductRepository(session=session)
    return ProductService(repo=repo)


ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]
