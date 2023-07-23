from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_session
from main import app
from models.dish import Dish
from schemas import dish

router = APIRouter()


@app.get("/", response_model=list[Dish])
async def get_all(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Dish))
    return result.scalars().all()


@app.get("/{id}", response_model=Dish)
async def get(id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Dish).where(Dish.id == id))
    return result.scalars().first()


@app.post("/", response_model=Dish)
async def create(
    dish: dish.DishCreate, session: AsyncSession = Depends(get_session)
):
    new_dish = Dish(**dish)
    session.add(new_dish)
    await session.commit()
    await session.refresh(new_dish)
    return new_dish


@app.delete("/{id}", response_model=Dish)
async def delete(id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Dish).where(Dish.id == id))
    dish = result.scalars().first()
    await session.delete(dish)
    await session.commit()
    return dish
