from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .manager import db_manager

SessionDep = Annotated[AsyncSession, Depends(db_manager.get_session)]
