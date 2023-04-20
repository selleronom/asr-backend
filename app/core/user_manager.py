import uuid
from typing import Optional

from app.api.deps import get_user_db
from app.core import auth
from app.models import UserTable
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase


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


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[UserTable, uuid.UUID](
    get_user_manager,  # type: ignore
    [auth.AUTH_BACKEND],
)

get_current_user = fastapi_users.current_user()
get_current_active_user = fastapi_users.current_user(active=True)
get_current_superuser = fastapi_users.current_user(active=True, superuser=True)
