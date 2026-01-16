from src.service import BaseService

from .model import User
from .repo import UserRepository
from .schema import UserCreateSchema


class UserService(
    BaseService[
        UserCreateSchema,
        UserRepository,
        User,
    ]
): ...
