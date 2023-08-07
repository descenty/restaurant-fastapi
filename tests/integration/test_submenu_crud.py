import pytest
from httpx import AsyncClient

from main import app

pytestmark = pytest.mark.anyio


class TestSubmenuCRUD:
    menu_id: str
    menu_title: str
    menu_description: str
    submenu_id: str
    submenu_title: str
    submenu_description: str

    async def test_create_menu(self, async_client):
        response = await async_client.post(
            app.url_path_for('create_menu'),
            json={
                'title': 'My menu 1',
                'description': 'My menu description 1',
            },
        )
        assert response.status_code == 201
        body = response.json()
        self.__class__.menu_id = body['id']
        assert body['id'] == self.__class__.menu_id

    async def test_get_all(self, async_client: AsyncClient):
        response = await async_client.get(
            app.url_path_for('get_all_submenus', menu_id=self.__class__.menu_id)
        )
        assert response.status_code == 200
        assert response.json() == []

    async def test_create(self, async_client):
        response = await async_client.post(
            app.url_path_for('create_submenu', menu_id=self.__class__.menu_id),
            json={
                'title': 'My submenu 1',
                'description': 'My submenu description 1',
            },
        )
        assert response.status_code == 201
        body = response.json()
        self.__class__.submenu_id = body['id']
        self.__class__.submenu_title = body['title']
        self.__class__.submenu_description = body['description']
        assert body['id'] == self.__class__.submenu_id
        assert body['title'] == self.__class__.submenu_title
        assert body['description'] == self.__class__.submenu_description

    async def test_get_all_after_create(self, async_client: AsyncClient):
        response = await async_client.get(
            app.url_path_for('get_all_submenus', menu_id=self.__class__.menu_id)
        )
        assert response.status_code == 200
        assert response.json() != []

    async def test_get(self, async_client: AsyncClient):
        response = await async_client.get(
            app.url_path_for(
                'get_submenu',
                menu_id=self.__class__.menu_id,
                id=self.__class__.submenu_id,
            )
        )
        assert response.status_code == 200
        body = response.json()
        assert body['id'] == self.__class__.submenu_id
        assert body['title'] == self.__class__.submenu_title
        assert body['description'] == self.__class__.submenu_description

    async def test_update(self, async_client: AsyncClient):
        response = await async_client.patch(
            app.url_path_for(
                'update_submenu',
                menu_id=self.__class__.menu_id,
                id=self.__class__.submenu_id,
            ),
            json={
                'title': 'My updated submenu 1',
                'description': 'My updated submenu description 1',
            },
        )
        assert response.status_code == 200
        body = response.json()
        assert body['title'] != self.__class__.submenu_title
        assert body['description'] != self.__class__.submenu_description
        self.__class__.submenu_title = body['title']
        self.__class__.submenu_description = body['description']
        assert body['title'] == self.__class__.submenu_title
        assert body['description'] == self.__class__.submenu_description

    async def test_get_after_update(self, async_client: AsyncClient):
        response = await async_client.get(
            app.url_path_for(
                'get_submenu',
                menu_id=self.__class__.menu_id,
                id=self.__class__.submenu_id,
            )
        )
        assert response.status_code == 200
        body = response.json()
        assert body['id'] == self.__class__.submenu_id
        assert body['title'] == self.__class__.submenu_title
        assert body['description'] == self.__class__.submenu_description

    async def test_delete(self, async_client: AsyncClient):
        response = await async_client.delete(
            app.url_path_for(
                'delete_submenu',
                menu_id=self.__class__.menu_id,
                id=self.__class__.submenu_id,
            )
        )
        assert response.status_code == 200

    async def test_get_all_after_delete(self, async_client: AsyncClient):
        response = await async_client.get(
            app.url_path_for('get_all_submenus', menu_id=self.__class__.menu_id)
        )
        assert response.status_code == 200
        assert response.json() == []

    async def test_get_after_delete(self, async_client: AsyncClient):
        response = await async_client.get(
            app.url_path_for(
                'get_submenu',
                menu_id=self.__class__.menu_id,
                id=self.__class__.submenu_id,
            )
        )
        assert response.status_code == 404
        assert response.json()['detail'] == 'submenu not found'

    async def test_delete_menu(self, async_client: AsyncClient):
        response = await async_client.delete(
            app.url_path_for('delete_menu', id=self.__class__.menu_id)
        )
        assert response.status_code == 200

    async def test_get_all_menus_after_delete(self, async_client: AsyncClient):
        response = await async_client.get(app.url_path_for('get_all_menus'))
        assert response.status_code == 200
        assert response.json() == []
