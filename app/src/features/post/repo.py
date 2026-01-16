from src.repo import BaseRepository

from .model import Post


class PostRepository(BaseRepository[Post]):
    model = Post
    order_by = [Post.id]
