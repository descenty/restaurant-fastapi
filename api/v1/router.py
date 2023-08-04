from fastapi import APIRouter

from .endpoints import menus
from .endpoints import submenus
from .endpoints import dishes


api_router = APIRouter()
api_router.include_router(menus.router, prefix="/menus", tags=["menus"])
api_router.include_router(submenus.router, prefix="/menus", tags=["submenus"])
api_router.include_router(dishes.router, prefix="/menus", tags=["dishes"])
