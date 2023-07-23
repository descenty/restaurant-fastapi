from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_session
from main import app
from models.menu import Menu
from schemas import menu

router = APIRouter()


@app.get("/", response_model=list[Menu])
async def get_all(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Menu))
    return result.scalars().all()


@app.get("/{id}", response_model=Menu)
async def get(id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Menu).where(Menu.id == id))
    return result.scalars().first()


@app.post("/", response_model=Menu)
async def create(
    menu: menu.MenuCreate, session: AsyncSession = Depends(get_session)
):
    new_menu = Menu(**menu)
    session.add(new_menu)
    await session.commit()
    await session.refresh(new_menu)
    return new_menu


@app.delete("/{id}", response_model=Menu)
async def delete(id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Menu).where(Menu.id == id))
    menu = result.scalars().first()
    await session.delete(menu)
    await session.commit()
    return menu
