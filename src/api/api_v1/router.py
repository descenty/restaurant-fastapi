from fastapi import APIRouter

from .endpoints import menus, submenus, dishes

api_router = APIRouter()
api_router.include_router(menus.router, prefix="/menus", tags=["menus"])
api_router.include_router(
    submenus.router, prefix="/submenus", tags=["submenus"]
)
api_router.include_router(dishes.router, prefix="/dishes", tags=["dishes"])
