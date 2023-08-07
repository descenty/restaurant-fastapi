from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from schemas.menu import MenuCreate, MenuDTO
from services.menu_service import MenuService, menu_service

router = APIRouter()


@router.get('', response_model=list[MenuDTO], name='get_all_menus')
async def get_all_menus(service: MenuService = Depends(menu_service)):
    return await service.get_all()


@router.get('/{id}', response_model=MenuDTO, name='get_menu')
async def get_menu(id: UUID, service: MenuService = Depends(menu_service)):
    if not (menu := await service.get(id)):
        raise HTTPException(status_code=404, detail='menu not found')
    return menu


@router.post('', response_model=MenuDTO, status_code=201, name='create_menu')
async def create_menu(
    menu_create: MenuCreate, service: MenuService = Depends(menu_service)
):
    return await service.create(menu_create)


@router.patch('/{id}', response_model=MenuDTO, name='update_menu')
async def update_menu(
    id: UUID,
    menu_create: MenuCreate,
    service: MenuService = Depends(menu_service),
):
    if not (menu := await service.update(id, menu_create)):
        raise HTTPException(status_code=404, detail='menu not found')
    return menu


@router.delete('/{id}', response_model=UUID, name='delete_menu')
async def delete_menu(id: UUID, service: MenuService = Depends(menu_service)):
    if not (deleted_id := await service.delete(id)):
        raise HTTPException(status_code=404, detail='menu not found')
    return deleted_id
