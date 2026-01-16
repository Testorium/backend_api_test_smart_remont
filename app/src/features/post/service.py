from src.service import BaseService

from .model import Post
from .repo import PostRepository
from .schema import PostCreateSchema


class PostService(
    BaseService[
        PostCreateSchema,
        PostRepository,
        Post,
    ]
): ...
