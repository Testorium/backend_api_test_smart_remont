# TODO: add
# upsert()
# upsert_many()
# delete()
# delete_many()
# delete_where()

# TODO: add conditions to every method it can be added


from collections.abc import Iterable
from typing import Any, List, Literal, Optional, Sequence, Type, Union, cast

from sqlalchemy import ColumnElement, Result, Select, UnaryExpression, func, select
from sqlalchemy import exists as sql_exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql.selectable import ForUpdateParameter

from .constants import DEFAULT_ERROR_MESSAGE_TEMPLATES
from .exceptions import ErrorMessages, NotFoundError, wrap_sqlalchemy_exception
from .types import LoadOptions, OrderByExpr, StatementTypeT


class BaseRepository[ModelT]:
    model: Type[ModelT]

    order_by: Iterable[OrderByExpr] | None = None
    """Default ordering expressions for select queries."""

    error_messages: Optional[ErrorMessages] = None
    """Default error messages for the repository."""

    def __init__(
        self,
        session: AsyncSession,
        auto_refresh: bool = True,
        auto_commit: bool = False,
        error_messages: Optional[ErrorMessages] = None,
        order_by: Iterable[OrderByExpr] | None = None,
    ) -> None:
        self.auto_refresh = auto_refresh
        self.auto_commit = auto_commit
        self.session = session

        self.order_by = order_by if order_by is not None else self.order_by

        self.error_messages = self._get_error_messages(
            error_messages=error_messages,
            default_messages=self.error_messages,
        )

    async def _flush_or_commit(self, auto_commit: Optional[bool]) -> Any | None:
        if auto_commit is None:
            auto_commit = self.auto_commit

        return (
            await self.session.commit() if auto_commit else await self.session.flush()
        )

    async def _execute(
        self,
        statement: Select[Any],
        uniquify: bool = False,
    ) -> Result[Any]:
        result = await self.session.execute(statement)

        if uniquify:
            result = result.unique()

        return result

    async def _attach_to_session(
        self,
        model: ModelT,
        strategy: Literal["add", "merge"] = "add",
        load: bool = True,
    ) -> ModelT:
        if strategy == "add":
            self.session.add(model)
            return model
        if strategy == "merge":
            return await self.session.merge(model, load=load)  # type: ignore
        msg = "Unexpected value for `strategy`, must be `'add'` or `'merge'`"  # type: ignore[unreachable]
        raise ValueError(msg)

    async def _refresh(
        self,
        instance: ModelT,
        auto_refresh: Optional[bool],
        attribute_names: Optional[Iterable[str]] = None,
        with_for_update: ForUpdateParameter = None,
    ) -> Any | None:
        if auto_refresh is None:
            auto_refresh = self.auto_refresh

        return (
            await self.session.refresh(
                instance=instance,
                attribute_names=attribute_names,
                with_for_update=with_for_update,
            )
            if auto_refresh
            else None
        )

    async def add(
        self,
        data: ModelT,
        *,
        auto_commit: Optional[bool] = None,
        auto_refresh: Optional[bool] = None,
        attribute_names: Optional[Iterable[str]] = None,
        error_messages: Optional[ErrorMessages | None] = None,
    ) -> ModelT:
        error_messages = self._get_error_messages(
            error_messages=error_messages,
            default_messages=self.error_messages,
        )
        with wrap_sqlalchemy_exception(error_messages=error_messages):
            instance = await self._attach_to_session(data)
            await self._flush_or_commit(auto_commit=auto_commit)
            await self._refresh(
                instance,
                attribute_names=attribute_names,
                auto_refresh=auto_refresh,
            )
            return instance

    async def add_many(
        self,
        data: List[ModelT],
        *,
        auto_commit: Optional[bool] = None,
        error_messages: Optional[ErrorMessages | None] = None,
    ) -> Sequence[ModelT]:
        error_messages = self._get_error_messages(
            error_messages=error_messages,
            default_messages=self.error_messages,
        )
        with wrap_sqlalchemy_exception(error_messages=error_messages):
            self.session.add_all(data)
            await self._flush_or_commit(auto_commit=auto_commit)
            return data

    async def list(
        self,
        uniquify: Optional[bool] = False,
        load_options: Optional[LoadOptions] = None,
        order_by: Iterable[OrderByExpr] | None = None,
        error_messages: Optional[ErrorMessages | None] = None,
        **kwargs: Any,
    ) -> Sequence[ModelT]:
        # TODO: apply pagination filters

        error_messages = self._get_error_messages(
            error_messages=error_messages,
            default_messages=self.error_messages,
        )
        with wrap_sqlalchemy_exception(error_messages=error_messages):
            statement = select(self.model)

            if order_by is None:
                order_by = self.order_by if self.order_by is not None else []

            statement = self._apply_order_by(statement=statement, order_by=order_by)
            statement = self._apply_select_filters_by_kwargs(statement, **kwargs)
            statement = self._apply_load_options(statement, load_options)
            result = await self._execute(statement, uniquify=uniquify)
            instances = result.scalars().all()
            return instances

    async def get_one(
        self,
        uniquify: Optional[bool] = False,
        load_options: Optional[LoadOptions] = None,
        error_messages: Optional[ErrorMessages | None] = None,
        **kwargs: Any,
    ) -> ModelT:
        error_messages = self._get_error_messages(
            error_messages=error_messages,
            default_messages=self.error_messages,
        )
        with wrap_sqlalchemy_exception(error_messages=error_messages):
            statement = select(self.model)

            statement = self._apply_select_filters_by_kwargs(statement, **kwargs)
            statement = self._apply_load_options(statement, load_options)

            instance = (
                await self._execute(statement, uniquify=uniquify)
            ).scalar_one_or_none()
            instance = self.check_not_found(instance)
            return instance

    async def get_one_or_none(
        self,
        uniquify: Optional[bool] = False,
        load_options: Optional[LoadOptions] = None,
        error_messages: Optional[ErrorMessages | None] = None,
        **kwargs: Any,
    ) -> ModelT | None:
        error_messages = self._get_error_messages(
            error_messages=error_messages,
            default_messages=self.error_messages,
        )
        with wrap_sqlalchemy_exception(error_messages=error_messages):
            statement = select(self.model)

            statement = self._apply_select_filters_by_kwargs(statement, **kwargs)
            statement = self._apply_load_options(statement, load_options)

            instance = cast(
                "Result[tuple[ModelT]]",
                (await self._execute(statement, uniquify=uniquify)),
            ).scalar_one_or_none()

            return instance

    async def update(
        self,
        instance: ModelT,
        *,
        auto_commit: Optional[bool] = None,
        auto_refresh: Optional[bool] = None,
        attribute_names: Optional[Iterable[str]] = None,
        with_for_update: ForUpdateParameter = None,
        error_messages: Optional[ErrorMessages | None] = None,
    ) -> ModelT:
        error_messages = self._get_error_messages(
            error_messages=error_messages,
            default_messages=self.error_messages,
        )
        with wrap_sqlalchemy_exception(error_messages=error_messages):
            instance = await self._attach_to_session(
                instance,
                strategy="merge",
            )

            await self._flush_or_commit(auto_commit=auto_commit)
            await self._refresh(
                instance,
                attribute_names=attribute_names,
                with_for_update=with_for_update,
                auto_refresh=auto_refresh,
            )
            return instance

    async def update_many(
        self,
        instances: Iterable[ModelT],
        *,
        auto_commit: Optional[bool] = None,
        auto_refresh: Optional[bool] = None,
        attribute_names: Optional[Iterable[str]] = None,
        with_for_update: ForUpdateParameter = None,
        error_messages: Optional[ErrorMessages | None] = None,
    ) -> Sequence[ModelT]:
        error_messages = self._get_error_messages(
            error_messages=error_messages,
            default_messages=self.error_messages,
        )

        with wrap_sqlalchemy_exception(error_messages=error_messages):
            merged_instances: list[ModelT] = []

            for instance in instances:
                merged = await self._attach_to_session(
                    instance,
                    strategy="merge",
                )
                merged_instances.append(merged)

            await self._flush_or_commit(auto_commit=auto_commit)

            for instance in merged_instances:
                await self._refresh(
                    instance,
                    attribute_names=attribute_names,
                    with_for_update=with_for_update,
                    auto_refresh=auto_refresh,
                )

            return merged_instances

    async def count(
        self,
        conditions: Optional[Iterable[ColumnElement[bool]]] = None,
        error_messages: Optional[ErrorMessages] = None,
        **kwargs: Any,
    ) -> int:
        error_messages = self._get_error_messages(
            error_messages=error_messages,
            default_messages=self.error_messages,
        )

        with wrap_sqlalchemy_exception(error_messages=error_messages):
            statement = select(func.count()).select_from(self.model)
            statement = self._apply_conditions(statement, conditions)
            statement = self._apply_select_filters_by_kwargs(statement, **kwargs)

            result = await self._execute(statement)
            return result.scalar_one()

    async def exists(
        self,
        conditions: Optional[Iterable[ColumnElement[bool]]] = None,
        error_messages: Optional[ErrorMessages | None] = None,
    ) -> bool:
        error_messages = self._get_error_messages(
            error_messages=error_messages,
            default_messages=self.error_messages,
        )

        with wrap_sqlalchemy_exception(error_messages=error_messages):
            subquery = select(1).select_from(self.model)
            subquery = self._apply_conditions(subquery, conditions)

            statement = select(sql_exists(subquery))

            result = await self.session.execute(statement)
            return bool(result.scalar())

    # @staticmethod
    # def _apply_pagination_filters(
    #     statement: StatementTypeT,
    #     **filters: Any,
    # ) -> StatementTypeT:
    #     pass

    @staticmethod
    def check_not_found(item_or_none: Optional[ModelT]) -> ModelT:
        if item_or_none is None:
            msg = "No item found when one was expected"
            raise NotFoundError(msg)
        return item_or_none

    # @staticmethod
    # def _get_instrumented_attr(
    #     model: ModelT,
    #     key: str | InstrumentedAttribute[Any],
    # ) -> InstrumentedAttribute[Any]:
    #     if isinstance(key, str):
    #         return cast("InstrumentedAttribute[Any]", getattr(model, key))
    #     return key

    @staticmethod
    def _apply_conditions(
        statement: StatementTypeT,
        conditions: Iterable[ColumnElement[bool]] | None,
    ) -> StatementTypeT:
        if not conditions:
            return statement

        return statement.where(*conditions)

    @staticmethod
    def _get_error_messages(
        error_messages: Optional[ErrorMessages | None] = None,
        default_messages: Optional[ErrorMessages | None] = None,
    ) -> ErrorMessages:
        messages = cast("ErrorMessages", dict(DEFAULT_ERROR_MESSAGE_TEMPLATES))

        if default_messages:
            messages.update(default_messages)

        if error_messages:
            messages.update(error_messages)

        return messages

    @staticmethod
    def _apply_load_options(
        statement: StatementTypeT,
        load_options: Optional[LoadOptions] = None,
    ) -> StatementTypeT:
        if not load_options:
            return statement

        return statement.options(*load_options)

    @staticmethod
    def _apply_select_filters_by_kwargs(
        statement: StatementTypeT,
        **kwargs: Any,
    ) -> StatementTypeT:
        if not kwargs:
            return statement
        return cast("StatementTypeT", statement.filter_by(**kwargs))

    @staticmethod
    def _apply_order_by(
        statement: StatementTypeT,
        order_by: Iterable[OrderByExpr] | None = None,
    ) -> StatementTypeT:
        if not isinstance(statement, Select) or not order_by:
            return statement

        for order_field in order_by:
            if isinstance(order_field, UnaryExpression):
                statement = statement.order_by(order_field)
            else:
                statement = statement.order_by(order_field.asc())
        return statement

    @classmethod
    def get_id_attribute_value(
        cls,
        item: Union[ModelT, type[ModelT]],
        id_attribute: Optional[Union[str, InstrumentedAttribute[Any]]] = None,
    ) -> Any:
        if isinstance(id_attribute, InstrumentedAttribute):
            id_attribute = id_attribute.key
        return getattr(
            item, id_attribute if id_attribute is not None else cls.id_attribute
        )
