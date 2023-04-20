"""
Users and auth routers 'for free' from FastAPI Users.
https://fastapi-users.github.io/fastapi-users/configuration/routers/

You can include more of them + oauth login endpoints.

fastapi_users in defined in deps, because it also
includes useful dependencies.
"""


from app.api.endpoints import auth, users, items
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/backend/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/backend/users", tags=["users"])
api_router.include_router(items.router, prefix="/backend/items", tags=["items"])
