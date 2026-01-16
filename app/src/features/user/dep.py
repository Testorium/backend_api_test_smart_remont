from typing import Annotated

from fastapi import Depends
from src.database import SessionDep

from .repo import UserRepository
from .service import UserService


def get_user_service(session: SessionDep) -> UserService:
    repo = UserRepository(session=session)
    return UserService(repo=repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
