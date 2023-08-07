import uuid
from decimal import Decimal
from functools import lru_cache

import pytest
from httpx import AsyncClient

from main import app
from schemas.dish import DishCreate, DishDTO
from schemas.menu import MenuDTO
from schemas.submenu import SubmenuDTO
from services.dish_service import dish_service
from tests.api.mocks.dish_service import DishServiceMock

pytestmark = pytest.mark.anyio

menus = [
    MenuDTO(
        id=uuid.uuid4(),
        title='Menu 1',
        description='Menu 1 description',
        submenus_count=1,
        dishes_count=2,
    ),
]


submenus = [
    SubmenuDTO(
        id=uuid.uuid4(),
        title='Menu 1',
        description='Menu 1 description',
        menu_id=menus[0].id,
        dishes_count=2,
    ),
]


dishes = [
    DishDTO(
        id=uuid.uuid4(),
        title='Dish 1',
        description='Dish 1 description',
        price=Decimal('249.00'),
        submenu_id=submenus[0].id,
    ),
    DishDTO(
        id=uuid.uuid4(),
        title='Dish 2',
        description='Dish 2 description',
        price=Decimal('379.00'),
        submenu_id=submenus[0].id,
    ),
]


@lru_cache
def dish_service_mock() -> DishServiceMock:
    return DishServiceMock(menus, submenus, dishes)


def setup_module():
    app.dependency_overrides[dish_service] = dish_service_mock


async def test_get_all(async_client: AsyncClient):
    response = await async_client.get(
        app.url_path_for(
            'get_all_dishes', menu_id=menus[0].id, submenu_id=submenus[0].id
        )
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_one(async_client: AsyncClient):
    response = await async_client.get(
        app.url_path_for(
            'get_dish', menu_id=menus[0].id, submenu_id=submenus[0].id, id=dishes[0].id
        )
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


async def test_get_one_not_found(async_client: AsyncClient):
    response = await async_client.get(
        app.url_path_for(
            'get_dish', menu_id=menus[0].id, submenu_id=submenus[0].id, id=uuid.uuid4()
        )
    )
    assert response.status_code == 404
    assert response.json()['detail'] == 'dish not found'


async def test_create(async_client: AsyncClient):
    response = await async_client.post(
        app.url_path_for('create_dish', menu_id=menus[0].id, submenu_id=submenus[0].id),
        json=DishCreate(
            title='Dish 3',
            description='Dish 3 description',
            price=Decimal('149.00'),
        ).model_dump(mode='json'),
    )
    assert response.status_code == 201
    assert isinstance(response.json(), dict)


async def test_update(async_client: AsyncClient):
    response = await async_client.patch(
        app.url_path_for(
            'update_dish',
            menu_id=menus[0].id,
            submenu_id=submenus[0].id,
            id=dishes[0].id,
        ),
        json=DishCreate(
            title='Dish 3',
            description='Dish 3 description',
            price=Decimal('149.00'),
        ).model_dump(mode='json'),
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


async def test_update_not_found(async_client: AsyncClient):
    response = await async_client.patch(
        app.url_path_for(
            'update_dish',
            menu_id=menus[0].id,
            submenu_id=submenus[0].id,
            id=uuid.uuid4(),
        ),
        json=DishCreate(
            title='Dish 3',
            description='Dish 3 description',
            price=Decimal('149.00'),
        ).model_dump(mode='json'),
    )
    assert response.status_code == 404
    assert response.json()['detail'] == 'dish not found'


async def test_delete(async_client: AsyncClient):
    response = await async_client.delete(
        app.url_path_for(
            'delete_dish',
            menu_id=menus[0].id,
            submenu_id=submenus[0].id,
            id=dishes[0].id,
        )
    )
    assert response.status_code == 200
    assert isinstance(response.json(), str)


async def test_delete_not_found(async_client: AsyncClient):
    response = await async_client.delete(
        app.url_path_for(
            'delete_dish',
            menu_id=menus[0].id,
            submenu_id=submenus[0].id,
            id=uuid.uuid4(),
        )
    )
    assert response.status_code == 404
    assert response.json()['detail'] == 'dish not found'
