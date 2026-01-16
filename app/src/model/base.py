from humps import decamelize
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr
from src.database.config import db_config


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(naming_convention=db_config.naming_convention)

    @declared_attr.directive  # type: ignore
    def __tablename__(cls) -> str:
        return f"{decamelize(cls.__name__)}s"
