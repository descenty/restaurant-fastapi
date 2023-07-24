from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_session
from models import Menu, Submenu, Dish
from schemas.submenu import SubmenuDTO, SubmenuCreate

router = APIRouter()


@router.get("/{menu_id}/submenus", response_model=list[SubmenuDTO])
async def get_all(menu_id: str, session: AsyncSession = Depends(get_session)):
    return [
        SubmenuDTO.model_validate(
            menu.__dict__ | {"dishes_count": dishes_count}
        )
        for (menu, dishes_count) in (
            await session.execute(
                select(Submenu, func.count(Dish.id))
                .join(
                    Dish, onclause=Submenu.id == Dish.submenu_id, isouter=True
                )
                .where(Submenu.menu_id == menu_id)
                .group_by(Submenu.id)
            )
        )
    ]


@router.get("/{menu_id}/submenus/{id}", response_model=SubmenuDTO)
async def get(
    menu_id: str, id: str, session: AsyncSession = Depends(get_session)
):
    if row := (
        await session.execute(
            select(Submenu, func.count(Dish.id))
            .join(Dish, onclause=Submenu.id == Dish.submenu_id, isouter=True)
            .where(Submenu.menu_id == menu_id, Submenu.id == id)
            .group_by(Submenu.id)
        )
    ).first():
        submenu, dishes_count = row
        return SubmenuDTO.model_validate(
            submenu.__dict__ | {"dishes_count": dishes_count}
        )
    raise HTTPException(status_code=404, detail="submenu not found")


@router.post("/{menu_id}/submenus", response_model=SubmenuDTO, status_code=201)
async def create(
    menu_id: str,
    submenu_create: SubmenuCreate,
    session: AsyncSession = Depends(get_session),
):
    if not (
        await session.scalars(
            select(Menu).where(
                Menu.id == menu_id,
            )
        )
    ).first():
        raise HTTPException(status_code=404, detail="menu not found")
    submenu = Submenu(menu_id=menu_id, **submenu_create.model_dump())
    session.add(submenu)
    await session.commit()
    await session.refresh(submenu)
    return SubmenuDTO.model_validate(submenu.__dict__ | {"dishes_count": 0})


@router.patch("/{menu_id}/submenus/{id}", response_model=SubmenuDTO)
async def update(
    menu_id: str,
    id: str,
    submenu_create: SubmenuCreate,
    session: AsyncSession = Depends(get_session),
):
    if row := (
        await session.execute(
            select(Submenu, func.count(Dish.id))
            .join(Dish, onclause=Submenu.id == Dish.submenu_id, isouter=True)
            .where(
                Submenu.menu_id == menu_id,
                Submenu.id == id,
            )
            .group_by(Submenu.id)
        )
    ).first():
        submenu, dishes_count = row
        for var, value in submenu_create.model_dump().items():
            setattr(submenu, var, value)
        await session.commit()
        await session.refresh(submenu)
        return SubmenuDTO.model_validate(
            submenu.__dict__ | {"dishes_count": dishes_count}
        )
    raise HTTPException(status_code=404, detail="submenu not found")


@router.delete("/{menu_id}/submenus/{id}", response_model=SubmenuDTO)
async def delete(
    menu_id: str, id: str, session: AsyncSession = Depends(get_session)
):
    if row := (
        await session.execute(
            select(Submenu, func.count(Dish.id))
            .join(Dish, onclause=Submenu.id == Dish.submenu_id, isouter=True)
            .where(
                Submenu.menu_id == menu_id,
                Submenu.id == id,
            )
            .group_by(Submenu.id)
        )
    ).first():
        submenu, dishes_count = row
        await session.delete(submenu)
        await session.commit()
        return SubmenuDTO.model_validate(
            submenu.__dict__ | {"dishes_count": dishes_count}
        )
    raise HTTPException(status_code=404, detail="submenu not found")
