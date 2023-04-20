from app.core import auth
from app.core.user_manager import fastapi_users
from app.schemas import UserCreate, UserRead
from fastapi import APIRouter

router = APIRouter()
router.include_router(
    fastapi_users.get_auth_router(auth.AUTH_BACKEND), prefix="/jwt", tags=["auth"]
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="",
    tags=["auth"],
)
