from fastapi import APIRouter, Depends, HTTPException
from schemas.menu import MenuDTO
from repository.menu import MenuRepository
from uuid import UUID

router = APIRouter()


@router.get("", response_model=list[MenuDTO])
async def get_all(
    menus: list[MenuDTO] = Depends(MenuRepository.read_all),
):
    return menus


@router.get("/{id}", response_model=MenuDTO)
async def get(menu: MenuDTO | None = Depends(MenuRepository.read)):
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return menu


@router.post("", response_model=MenuDTO, status_code=201)
async def create(menu: MenuDTO = Depends(MenuRepository.create)):
    return menu


@router.patch("/{id}", response_model=MenuDTO)
async def update(menu: MenuDTO | None = Depends(MenuRepository.update)):
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return menu


@router.delete("/{id}")
async def delete(deleted_id: UUID | None = Depends(MenuRepository.delete)):
    if deleted_id is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return deleted_id
