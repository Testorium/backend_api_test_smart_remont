from typing import TYPE_CHECKING

from fastapi import Request, status
from fastapi.responses import JSONResponse
from src.repo.exceptions import (
    DuplicateKeyError,
    IntegrityError,
    NotFoundError,
    RepositoryError,
)

if TYPE_CHECKING:
    from fastapi import FastAPI


async def duplicate_key_exception_handler(
    request: Request,
    exc: DuplicateKeyError,
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


async def integrity_exception_handler(
    request: Request,
    exc: IntegrityError,
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


async def not_found_exception_handler(
    request: Request,
    exc: NotFoundError,
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


async def repository_exception_handler(
    request: Request,
    exc: RepositoryError,
):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc)},
    )


def register_exception_handlers(app: "FastAPI"):
    app.add_exception_handler(DuplicateKeyError, duplicate_key_exception_handler)
    app.add_exception_handler(IntegrityError, integrity_exception_handler)
    app.add_exception_handler(NotFoundError, not_found_exception_handler)
    app.add_exception_handler(RepositoryError, repository_exception_handler)
