from typing import List

from fastapi import APIRouter
from src.routers import api_prefix_config

from .dep import UserServiceDep
from .schema import UserCreateSchema, UserReadSchema

router = APIRouter(prefix=api_prefix_config.v1.users, tags=["User"])


@router.post("/", response_model=UserReadSchema)
async def add_new_user(
    data: UserCreateSchema,
    service: UserServiceDep,
):
    return await service.add(data)


@router.get(
    "/",
    response_model=List[UserReadSchema],
)
async def list_users(
    service: UserServiceDep,
):
    return await service.list()
