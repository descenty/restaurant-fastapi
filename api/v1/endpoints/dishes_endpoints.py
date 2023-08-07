from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from schemas.dish import DishCreate, DishDTO
from services.dish_service import DishService, dish_service

router = APIRouter()


@router.get(
    '/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=list[DishDTO],
    name='get_all_dishes',
)
async def get_all_dishes(
    menu_id: UUID,
    submenu_id: UUID,
    service: DishService = Depends(dish_service),
):
    return await service.get_all(menu_id, submenu_id)


@router.get(
    '/{menu_id}/submenus/{submenu_id}/dishes/{id}',
    response_model=DishDTO,
    name='get_dish',
)
async def get_dish(
    menu_id: UUID,
    submenu_id: UUID,
    id: UUID,
    service: DishService = Depends(dish_service),
):
    if not (dish := await service.get(menu_id, submenu_id, id)):
        raise HTTPException(status_code=404, detail='dish not found')
    return dish


@router.post(
    '/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=DishDTO,
    status_code=201,
    name='create_dish',
)
async def create_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_create: DishCreate,
    service: DishService = Depends(dish_service),
):
    if not (dish := await service.create(menu_id, submenu_id, dish_create)):
        raise HTTPException(status_code=404, detail='submenu not found')
    return dish


@router.patch(
    '/{menu_id}/submenus/{submenu_id}/dishes/{id}',
    response_model=DishDTO,
    name='update_dish',
)
async def update_dish(
    menu_id: UUID,
    submenu_id: UUID,
    id: UUID,
    dish_create: DishCreate,
    service: DishService = Depends(dish_service),
):
    if not (dish := await service.update(menu_id, submenu_id, id, dish_create)):
        raise HTTPException(status_code=404, detail='dish not found')
    return dish


@router.delete(
    '/{menu_id}/submenus/{submenu_id}/dishes/{id}',
    response_model=UUID,
    name='delete_dish',
)
async def delete_dish(
    menu_id: UUID,
    submenu_id: UUID,
    id: UUID,
    service: DishService = Depends(dish_service),
):
    if not (deleted_id := await service.delete(menu_id, submenu_id, id)):
        raise HTTPException(status_code=404, detail='dish not found')
    return deleted_id
