from fastapi import APIRouter

from .endpoints import menus

api_router = APIRouter()
api_router.include_router(menus.router, prefix="/menus", tags=["menus"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])
