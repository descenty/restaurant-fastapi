from fastapi import APIRouter, Depends, HTTPException
from schemas.menu import MenuDTO
from repository.menu import MenuRepository

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


@router.delete("/{id}", response_model=MenuDTO)
async def delete(menu: MenuDTO | None = Depends(MenuRepository.delete)):
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return menu
