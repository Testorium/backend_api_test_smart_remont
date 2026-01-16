from collections.abc import Iterable
from typing import Any, TypeAlias, TypeVar, Union

from sqlalchemy import Delete, Select, UnaryExpression, Update
from sqlalchemy.orm import InstrumentedAttribute, Load
from sqlalchemy.sql.dml import ReturningDelete, ReturningUpdate

StatementTypeT = TypeVar(
    "StatementTypeT",
    bound=Union[
        ReturningDelete[tuple[Any]],
        ReturningUpdate[tuple[Any]],
        Select[tuple[Any]],
        Select[Any],
        Update,
        Delete,
    ],
)

OrderByExpr = Union[InstrumentedAttribute, UnaryExpression]
LoadOptions: TypeAlias = Iterable["Load[Any]"]
