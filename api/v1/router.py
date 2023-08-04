from fastapi import APIRouter

from .endpoints.menus import router as menus_router

# from .endpoints.submenus import SubmenuController
# from .endpoints.dishes import DishController


api_router = APIRouter()
api_router.include_router(menus_router, prefix="/menus", tags=["menus"])
# api_router.include_router(submenus.router, prefix="/menus", tags=["submenus"])
# api_router.include_router(dishes.router, prefix="/menus", tags=["dishes"])
