from src.repo import BaseRepository

from .model import User


class UserRepository(BaseRepository[User]):
    model = User
    order_by = [User.id]
