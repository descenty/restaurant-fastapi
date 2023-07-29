from fastapi import APIRouter, Depends, HTTPException
from schemas.dish import DishDTO
from repository.dish import DishRepository

router = APIRouter()


@router.get(
    "/{menu_id}/submenus/{submenu_id}/dishes", response_model=list[DishDTO]
)
async def get_all(
    dishes: list[DishDTO] = Depends(DishRepository.read_all),
):
    return dishes


@router.get(
    "/{menu_id}/submenus/{submenu_id}/dishes/{id}", response_model=DishDTO
)
async def get(dish: DishDTO | None = Depends(DishRepository.read)):
    if dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return dish


@router.post(
    "/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=DishDTO,
    status_code=201,
)
async def create(dish: DishDTO | None = Depends(DishRepository.create)):
    if dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return dish


@router.patch(
    "/{menu_id}/submenus/{submenu_id}/dishes/{id}", response_model=DishDTO
)
async def update(dish: DishDTO | None = Depends(DishRepository.update)):
    if dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return dish


@router.delete(
    "/{menu_id}/submenus/{submenu_id}/dishes/{id}", response_model=DishDTO
)
async def delete(dish: DishDTO | None = Depends(DishRepository.delete)):
    if dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return dish
