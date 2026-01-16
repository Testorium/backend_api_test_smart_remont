"""
This code is adapted and modified specifically for PostgreSQL usage from the
'advanced_alchemy' library originally developed by the Litestar organization.

All modifications are intended to simplify exception handling and repository
operations while retaining the core functionality provided by advanced_alchemy.
"""

import re
from collections.abc import Callable, Generator
from contextlib import contextmanager
from typing import Optional, TypedDict, cast

from sqlalchemy.exc import IntegrityError as SQLAlchemyIntegrityError
from sqlalchemy.exc import InvalidRequestError as SQLAlchemyInvalidRequestError
from sqlalchemy.exc import MultipleResultsFound, SQLAlchemyError, StatementError


class RepositoryError(Exception):
    """Base repository exception type."""


class IntegrityError(RepositoryError):
    """Data integrity error."""


class DuplicateKeyError(IntegrityError):
    """Duplicate key error."""


class ForeignKeyError(IntegrityError):
    """Foreign key error."""


class NotFoundError(RepositoryError):
    """Not found error.

    This exception is raised when a requested resource is not found.
    """


class MultipleResultsFoundError(RepositoryError):
    """Multiple results found error.

    This exception is raised when a single result was expected but multiple were found.
    """


class InvalidRequestError(RepositoryError):
    """Invalid request error.

    This exception is raised when SQLAlchemy is unable to complete the request due to a runtime error
    """


POSTGRES_DUPLICATE_KEY_REGEXES = [
    re.compile(
        r"^.*duplicate\s+key.*\"(?P<columns>[^\"]+)\"\s*\n.*Key\s+\((?P<key>.*)\)=\((?P<value>.*)\)\s+already\s+exists.*$"
    ),
    re.compile(r"^.*duplicate\s+key.*\"(?P<columns>[^\"]+)\"\s*\n.*$"),
]

POSTGRES_FOREIGN_KEY_REGEXES = [
    re.compile(
        r".*on table \"(?P<table>[^\"]+)\" violates "
        r"foreign key constraint \"(?P<constraint>[^\"]+)\".*\n"
        r"DETAIL:  Key \((?P<key>.+)\)=\(.+\) "
        r"is (not present in|still referenced from) table "
        r"\"(?P<key_table>[^\"]+)\"."
    ),
]

POSTGRES_CHECK_CONSTRAINT_REGEXES = [
    re.compile(
        r".*new row for relation \"(?P<table>.+)\" violates check constraint (?P<check_name>.+)"
    ),
]


class ErrorMessages(TypedDict, total=False):
    duplicate_key: str | Callable[[Exception], str]
    integrity: str | Callable[[Exception], str]
    foreign_key: str | Callable[[Exception], str]
    multiple_rows: str | Callable[[Exception], str]
    check_constraint: str | Callable[[Exception], str]
    other: str | Callable[[Exception], str]
    not_found: str | Callable[[Exception], str]


def _get_error_message(error_messages: ErrorMessages, key: str, exc: Exception) -> str:
    template: str | Callable[[Exception], str] = error_messages.get(
        key, f"{key} error: {exc}"
    )  # type: ignore[assignment]
    if callable(template):  # pyright: ignore[reportUnknownArgumentType]
        template = template(exc)  # pyright: ignore[reportUnknownVariableType]
    return template  # pyright: ignore[reportUnknownVariableType]


@contextmanager
def wrap_sqlalchemy_exception(  # noqa: C901, PLR0915
    error_messages: Optional[ErrorMessages] = None,
) -> Generator[None, None, None]:
    try:
        yield

    except NotFoundError as exc:
        if error_messages is not None:
            msg = _get_error_message(
                error_messages=error_messages,
                key="not_found",
                exc=exc,
            )
        else:
            msg = "No rows matched the specified data"
        raise NotFoundError(msg) from exc

    except MultipleResultsFound as exc:
        if error_messages is not None:
            msg = _get_error_message(
                error_messages=error_messages, key="multiple_rows", exc=exc
            )
        else:
            msg = "Multiple rows matched the specified data"
        raise MultipleResultsFoundError(msg) from exc

    except SQLAlchemyIntegrityError as exc:
        if error_messages is not None:
            keys_to_regex = {
                "duplicate_key": (POSTGRES_DUPLICATE_KEY_REGEXES, DuplicateKeyError),
                "check_constraint": (POSTGRES_CHECK_CONSTRAINT_REGEXES, IntegrityError),
                "foreign_key": (POSTGRES_FOREIGN_KEY_REGEXES, ForeignKeyError),
            }
            detail = (
                " - ".join(str(exc_arg) for exc_arg in exc.orig.args)
                if exc.orig.args
                else ""
            )

            for key, (regexes, exception) in keys_to_regex.items():
                for regex in regexes:
                    if (match := regex.findall(detail)) and match[0]:
                        raise exception(
                            _get_error_message(
                                error_messages=error_messages,
                                key=key,
                                exc=exc,
                            ),
                        ) from exc

            raise IntegrityError(
                _get_error_message(
                    error_messages=error_messages,
                    key="integrity",
                    exc=exc,
                ),
            ) from exc
        raise IntegrityError(f"An integrity error occurred: {exc}") from exc

    except SQLAlchemyInvalidRequestError as exc:
        print(str(exc))
        raise InvalidRequestError("An invalid request was made.") from exc

    except StatementError as exc:
        raise IntegrityError(
            cast(
                "str",
                getattr(
                    exc.orig, "detail", "There was an issue processing the statement."
                ),
            )
        ) from exc

    except SQLAlchemyError as exc:
        if error_messages is not None:
            msg = _get_error_message(
                error_messages=error_messages,
                key="other",
                exc=exc,
            )
        else:
            msg = f"An exception occurred: {exc}"
        raise RepositoryError(msg) from exc

    except AttributeError as exc:
        if error_messages is not None:
            msg = _get_error_message(
                error_messages=error_messages,
                key="other",
                exc=exc,
            )
        else:
            msg = f"An attribute error occurred during processing: {exc}"
        raise RepositoryError(msg) from exc
