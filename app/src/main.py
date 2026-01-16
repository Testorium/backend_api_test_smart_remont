from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from src.routers import main_router

from .database import db_manager


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield
    await db_manager.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(main_router)

# test


# DEFAULT_PAGINATION_SIZE: int = 20


# @dataclass
# class LimitOffset:
#     limit: int
#     """Maximum number of rows to return."""
#     offset: int
#     """Number of rows to skip before returning results."""

#     def append_to_statement(self, statement, model):
#         """Apply LIMIT/OFFSET pagination to the statement.

#         Args:
#             statement: The SQLAlchemy statement to modify
#             model: The SQLAlchemy model class

#         Returns:
#             StatementTypeT: Modified statement with limit and offset applied

#         Note:
#             Only modifies SELECT statements. Other statement types are returned as-is.

#         See Also:
#             :class:`sqlalchemy.sql.expression.Select`: SQLAlchemy SELECT statement
#         """
#         if isinstance(statement, Select):
#             return statement.limit(self.limit).offset(self.offset)
#         return statement


# def provide_limit_offset_pagination(
#     current_page: Annotated[
#         int,
#         Query(
#             ge=1,
#             alias="currentPage",
#             description="Page number for pagination.",
#         ),
#     ] = 1,
#     page_size: Annotated[
#         int,
#         Query(
#             ge=1,
#             alias="pageSize",
#             description="Number of items per page.",
#         ),
#     ] = DEFAULT_PAGINATION_SIZE,
# ) -> LimitOffset:
#     return LimitOffset(limit=page_size, offset=page_size * (current_page - 1))


# @app.get("/")
# def limit_offset(
#     limit_offset: Annotated[LimitOffset, Depends(provide_limit_offset_pagination)],
# ):
#     pass
