from typing import Annotated

from fastapi import Depends
from src.database import SessionDep

from .repo import PostRepository
from .service import PostService


def get_post_service(session: SessionDep) -> PostService:
    repo = PostRepository(session=session)
    return PostService(repo=repo)


PostServiceDep = Annotated[PostService, Depends(get_post_service)]
