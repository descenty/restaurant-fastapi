import uuid

import pytest
from httpx import AsyncClient

from main import app
from schemas.menu import MenuDTO
from schemas.submenu import SubmenuCreate, SubmenuDTO
from services.submenu_service import submenu_service
from tests.api.mocks.submenu_repository import SubmenuServiceMock

pytestmark = pytest.mark.anyio

menus = [
    MenuDTO(
        id=uuid.uuid4(),
        title='Menu 1',
        description='Menu 1 description',
        submenus_count=2,
        dishes_count=4,
    ),
]


submenus = [
    SubmenuDTO(
        id=uuid.uuid4(),
        title='Menu 1',
        description='Menu 1 description',
        menu_id=menus[0].id,
        dishes_count=3,
    ),
    SubmenuDTO(
        id=uuid.uuid4(),
        title='Menu 2',
        description='Menu 2 description',
        menu_id=menus[0].id,
        dishes_count=1,
    ),
]


def submenu_service_mock() -> SubmenuServiceMock:
    return SubmenuServiceMock(menus, submenus)


def setup_module():
    app.dependency_overrides[submenu_service] = submenu_service_mock


async def test_get_all(async_client: AsyncClient):
    response = await async_client.get(
        app.url_path_for('get_all_submenus', menu_id=menus[0].id)
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_one(async_client: AsyncClient):
    response = await async_client.get(
        app.url_path_for('get_submenu', menu_id=menus[0].id, id=submenus[0].id)
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


async def test_get_one_not_found(async_client: AsyncClient):
    response = await async_client.get(
        app.url_path_for('get_submenu', menu_id=menus[0].id, id=uuid.uuid4())
    )
    assert response.status_code == 404
    assert response.json()['detail'] == 'submenu not found'


async def test_create(async_client: AsyncClient):
    response = await async_client.post(
        app.url_path_for('create_submenu', menu_id=menus[0].id),
        json=SubmenuCreate(
            title='Submenu 3', description='Submenu 3 description'
        ).model_dump(mode='json'),
    )
    assert response.status_code == 201
    assert isinstance(response.json(), dict)


async def test_update(async_client: AsyncClient):
    response = await async_client.patch(
        app.url_path_for('update_submenu', menu_id=menus[0].id, id=submenus[0].id),
        json=SubmenuCreate(
            title='Submenu 3', description='Submenu 3 description'
        ).model_dump(mode='json'),
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


async def test_update_not_found(async_client: AsyncClient):
    response = await async_client.patch(
        app.url_path_for('update_submenu', menu_id=menus[0].id, id=uuid.uuid4()),
        json=SubmenuCreate(
            title='Submenu 3', description='Submenu 3 description'
        ).model_dump(mode='json'),
    )
    assert response.status_code == 404
    assert response.json()['detail'] == 'submenu not found'


async def test_delete(async_client: AsyncClient):
    response = await async_client.delete(
        app.url_path_for('delete_submenu', menu_id=menus[0].id, id=submenus[0].id)
    )
    assert response.status_code == 200
    assert isinstance(response.json(), str)


async def test_delete_not_found(async_client: AsyncClient):
    response = await async_client.delete(
        app.url_path_for('delete_submenu', menu_id=menus[0].id, id=uuid.uuid4())
    )
    assert response.status_code == 404
    assert response.json()['detail'] == 'submenu not found'
