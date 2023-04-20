"""
You can have several authentication methods, e.g. a cookie
authentication for browser-based queries and a JWT token authentication for pure API queries.

In this template, token will be sent through Bearer header
{"Authorization": "Bearer xyz"}
using JWT tokens.

There are more option to consider, refer to
https://fastapi-users.github.io/fastapi-users/configuration/authentication/

UserManager class is core fastapi users class with customizable attrs and methods
https://fastapi-users.github.io/fastapi-users/configuration/user-manager/
"""
import uuid
from typing import Optional

from app.api.deps import get_access_token_db
from app.models import AccessTokenTable, UserTable
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
)
from fastapi_users.authentication.strategy.db import (
    AccessTokenDatabase,
    DatabaseStrategy,
)
from fastapi_users.manager import BaseUserManager


def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessTokenTable] = Depends(
        get_access_token_db
    ),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=3600)


BEARER_TRANSPORT = CookieTransport(
    cookie_name="access_token",
    cookie_max_age=None,
    cookie_path="/",
    cookie_domain=None,
    cookie_secure=False,
    cookie_httponly=False,
)

AUTH_BACKEND = AuthenticationBackend(
    name="jwt",
    transport=BEARER_TRANSPORT,
    get_strategy=get_database_strategy,
)


class UserManager(UUIDIDMixin, BaseUserManager[UserTable, uuid.UUID]):
    reset_password_token_secret = "kSlYahkrsbtyXRprWQOwchcevyfmikrmSATQUPWQzPEtLvXTQp"
    verification_token_secret = "kSlYahkrsbtyXRprWQOwchcevyfmikrmSATQUPWQzPEtLvXTQp"

    async def on_after_register(
        self, user: UserTable, request: Optional[Request] = None
    ):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: UserTable, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: UserTable, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")
