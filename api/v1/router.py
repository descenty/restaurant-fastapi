from fastapi import APIRouter

from .endpoints import dishes_endpoints, menus_endpoints, submenus_endpoints

api_router = APIRouter()
api_router.include_router(
    menus_endpoints.router, prefix='/menus', tags=['menus']
)
api_router.include_router(
    submenus_endpoints.router, prefix='/menus', tags=['submenus']
)
api_router.include_router(
    dishes_endpoints.router, prefix='/menus', tags=['dishes']
)
