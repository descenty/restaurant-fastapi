from fastapi import APIRouter, Depends, HTTPException
from schemas.submenu import SubmenuDTO
from repository.submenu import SubmenuRepository
from uuid import UUID

router = APIRouter()


@router.get("/{menu_id}/submenus", response_model=list[SubmenuDTO])
async def get_all(
    submenus: list[SubmenuDTO] = Depends(SubmenuRepository.read_all),
):
    return submenus


@router.get("/{menu_id}/submenus/{id}", response_model=SubmenuDTO)
async def get(submenu: SubmenuDTO | None = Depends(SubmenuRepository.read)):
    if submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    return submenu


@router.post("/{menu_id}/submenus", response_model=SubmenuDTO, status_code=201)
async def create(
    submenu: SubmenuDTO | None = Depends(SubmenuRepository.create),
):
    if submenu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return submenu


@router.patch("/{menu_id}/submenus/{id}", response_model=SubmenuDTO)
async def update(
    submenu: SubmenuDTO | None = Depends(SubmenuRepository.update),
):
    if submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    return submenu


@router.delete("/{menu_id}/submenus/{id}")
async def delete(
    deleted_id: UUID | None = Depends(SubmenuRepository.delete),
):
    if deleted_id is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    return deleted_id
