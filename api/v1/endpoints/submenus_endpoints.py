from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from schemas.submenu import SubmenuCreate, SubmenuDTO
from services.submenu_service import SubmenuService, submenu_service

router = APIRouter()


@router.get(
    '/{menu_id}/submenus', response_model=list[SubmenuDTO], name='get_all_submenus'
)
async def get_all_submenus(
    menu_id: UUID, service: SubmenuService = Depends(submenu_service)
):
    return await service.get_all(menu_id)


@router.get('/{menu_id}/submenus/{id}', response_model=SubmenuDTO, name='get_submenu')
async def get_submenu(
    menu_id: UUID, id: UUID, service: SubmenuService = Depends(submenu_service)
):
    if not (submenu := await service.get(menu_id, id)):
        raise HTTPException(status_code=404, detail='submenu not found')
    return submenu


@router.post(
    '/{menu_id}/submenus',
    response_model=SubmenuDTO,
    status_code=201,
    name='create_submenu',
)
async def create_submenu(
    menu_id: UUID,
    submenu_create: SubmenuCreate,
    service: SubmenuService = Depends(submenu_service),
):
    if not (submenu := await service.create(menu_id, submenu_create)):
        raise HTTPException(status_code=404, detail='menu not found')
    return submenu


@router.patch(
    '/{menu_id}/submenus/{id}', response_model=SubmenuDTO, name='update_submenu'
)
async def update_submenu(
    menu_id: UUID,
    id: UUID,
    submenu_create: SubmenuCreate,
    service: SubmenuService = Depends(submenu_service),
):
    if not (submenu := await service.update(menu_id, id, submenu_create)):
        raise HTTPException(status_code=404, detail='submenu not found')
    return submenu


@router.delete('/{menu_id}/submenus/{id}', response_model=UUID, name='delete_submenu')
async def delete_submenu(
    menu_id: UUID, id: UUID, service: SubmenuService = Depends(submenu_service)
):
    if not (deleted_id := await service.delete(menu_id, id)):
        raise HTTPException(status_code=404, detail='submenu not found')
    return deleted_id
