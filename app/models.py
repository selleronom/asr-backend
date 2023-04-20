"""
SQL Alchemy models declaration.

Note, imported by alembic migrations logic, see `alembic/env.py`
"""

from typing import Any, cast

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTableUUID
from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy.orm.decl_api import declarative_base
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Integer, String

Base = cast(Any, declarative_base())


class UserTable(SQLAlchemyBaseUserTableUUID, Base):
    pass


class AccessTokenTable(SQLAlchemyBaseAccessTokenTableUUID, Base):
    pass


class ItemTable(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    user_id = Column(GUID, ForeignKey("user.id"))
    # user = relationship("User", back_populates="item")

    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    text = Column(String)
