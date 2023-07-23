from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from models.menu import Menu
from ..db.session import get_session


async def get_all(session: AsyncSession = Depends(get_session)) -> list[Menu]:
    result = await session.execute(select(City))
    return result.scalars().all()


async def get_biggest_cities(session: AsyncSession) -> list[City]:
    result = await session.execute(
        select(City).order_by(City.population.desc()).limit(20)
    )
    return result.scalars().all()


def add_city(session: AsyncSession, name: str, population: int):
    new_city = City(name=name, population=population)
    session.add(new_city)
    return new_city


"""
Пример контроллера

from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from fastapi_asyncalchemy.exceptions import DuplicatedEntryError
from fastapi_asyncalchemy.db.base import init_models
from fastapi_asyncalchemy.db.base import get_session
from fastapi_asyncalchemy import service


app = FastAPI()

# Dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


class CitySchema(BaseModel):
    name: str
    population: int


@app.get("/cities/biggest", response_model=list[CitySchema])
async def get_biggest_cities(session: AsyncSession = Depends(get_session)):
    cities = await service.get_biggest_cities(session)
    return [CitySchema(name=c.name, population=c.population) for c in cities]
"""
