from fastapi import APIRouter, Depends, HTTPException
from cache.redis import cached, invalidate
from schemas.menu import MenuCreate, MenuDTO
from services.menu import MenuService
from uuid import UUID

router = APIRouter()


@router.get("", response_model=list[MenuDTO])
@cached("menus")
async def get_all(service: MenuService = Depends(MenuService)):
    return await service.get_all()


@router.get("/{id}", response_model=MenuDTO)
@cached("menu-{id}")
async def get(id: UUID, service: MenuService = Depends(MenuService)):
    if not (menu := await service.get(id)):
        raise HTTPException(status_code=404, detail="menu not found")
    return menu


@router.post("", response_model=MenuDTO, status_code=201)
@invalidate("menus")
async def create(
    menu_create: MenuCreate, service: MenuService = Depends(MenuService)
):
    return await service.create(menu_create)


@router.patch("/{id}", response_model=MenuDTO)
@invalidate("menu-{id}")
async def update(
    id: UUID,
    menu_create: MenuCreate,
    service: MenuService = Depends(MenuService),
):
    if not (menu := await service.update(id, menu_create)):
        raise HTTPException(status_code=404, detail="menu not found")
    return menu


@router.delete("/{id}")
@invalidate("menu-{id}")
async def delete(id: UUID, service: MenuService = Depends(MenuService)):
    if not (deleted_id := await service.delete(id)):
        raise HTTPException(status_code=404, detail="menu not found")
    return deleted_id
