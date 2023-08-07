import uuid
from functools import lru_cache

import pytest
from httpx import AsyncClient

from main import app
from schemas.menu import MenuCreate, MenuDTO
from services.menu_service import menu_service
from tests.api.mocks.menu_service import MenuServiceMock

pytestmark = pytest.mark.anyio

menus = [
    MenuDTO(
        id=uuid.uuid4(),
        title='Menu 1',
        description='Menu 1 description',
        submenus_count=2,
        dishes_count=3,
    ),
    MenuDTO(
        id=uuid.uuid4(),
        title='Menu 2',
        description='Menu 2 description',
        submenus_count=2,
        dishes_count=3,
    ),
]


@lru_cache
def menu_service_mock() -> MenuServiceMock:
    return MenuServiceMock(menus)


def setup_module():
    app.dependency_overrides[menu_service] = menu_service_mock


async def test_get_all(async_client: AsyncClient):
    response = await async_client.get(app.url_path_for('get_all_menus'))
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_one(async_client: AsyncClient):
    response = await async_client.get(app.url_path_for('get_menu', id=menus[0].id))
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


async def test_get_one_not_found(async_client: AsyncClient):
    response = await async_client.get(app.url_path_for('get_menu', id=uuid.uuid4()))
    assert response.status_code == 404
    assert response.json()['detail'] == 'menu not found'


async def test_create(async_client: AsyncClient):
    response = await async_client.post(
        app.url_path_for('create_menu'),
        json=MenuCreate(title='Menu 3', description='Menu 3 description').model_dump(
            mode='json'
        ),
    )
    assert response.status_code == 201
    assert isinstance(response.json(), dict)


async def test_update(async_client: AsyncClient):
    response = await async_client.patch(
        app.url_path_for('update_menu', id=menus[0].id),
        json=MenuCreate(title='Menu 3', description='Menu 3 description').model_dump(
            mode='json'
        ),
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


async def test_update_not_found(async_client: AsyncClient):
    response = await async_client.patch(
        app.url_path_for('update_menu', id=uuid.uuid4()),
        json=MenuCreate(title='Menu 3', description='Menu 3 description').model_dump(
            mode='json'
        ),
    )
    assert response.status_code == 404
    assert response.json()['detail'] == 'menu not found'


async def test_delete(async_client: AsyncClient):
    response = await async_client.delete(
        app.url_path_for('delete_menu', id=menus[0].id)
    )
    assert response.status_code == 200
    assert isinstance(response.json(), str)


async def test_delete_not_found(async_client: AsyncClient):
    response = await async_client.delete(
        app.url_path_for('delete_menu', id=uuid.uuid4())
    )
    assert response.status_code == 404
    assert response.json()['detail'] == 'menu not found'
