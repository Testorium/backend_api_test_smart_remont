from fastapi import APIRouter
from src.routers import api_prefix_config

from .dep import PostServiceDep
from .schema import PostCreateSchema, PostReadSchema

router = APIRouter(prefix=api_prefix_config.v1.posts, tags=["Post"])


@router.post("/", response_model=PostReadSchema)
async def add_new_post(
    data: PostCreateSchema,
    service: PostServiceDep,
):
    return await service.add(data)
