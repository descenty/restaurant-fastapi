import pytest
from httpx import AsyncClient

from main import app

pytestmark = pytest.mark.anyio


class TestComputedFields:
    menu_id: str
    menu_title: str
    menu_description: str
    submenu_id: str
    submenu_title: str
    submenu_description: str
    dish_id: str
    dish_title: str
    dish_description: str
    dish_price: str

    async def test_create_menu(self, async_client: AsyncClient):
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

    async def test_create_submenu(self, async_client: AsyncClient):
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
        assert body['id'] == self.__class__.submenu_id

    async def test_create_dish1(self, async_client: AsyncClient):
        response = await async_client.post(
            app.url_path_for(
                'create_dish',
                menu_id=self.__class__.menu_id,
                submenu_id=self.__class__.submenu_id,
            ),
            json={
                'title': 'My dish 1',
                'description': 'My dish description 1',
                'price': '13.50',
            },
        )
        assert response.status_code == 201
        body = response.json()
        self.__class__.dish_id = body['id']
        assert body['id'] == self.__class__.dish_id

    async def test_create_dish2(self, async_client: AsyncClient):
        response = await async_client.post(
            app.url_path_for(
                'create_dish',
                menu_id=self.__class__.menu_id,
                submenu_id=self.__class__.submenu_id,
            ),
            json={
                'title': 'My dish 2',
                'description': 'My dish description 2',
                'price': '13.50',
            },
        )
        assert response.status_code == 201
        body = response.json()
        self.__class__.dish_id = body['id']
        assert body['id'] == self.__class__.dish_id

    async def test_get_menu(self, async_client: AsyncClient):
        response = await async_client.get(
            app.url_path_for('get_menu', id=self.__class__.menu_id)
        )
        assert response.status_code == 200
        body = response.json()
        assert body['id'] == self.__class__.menu_id
        assert body['submenus_count'] == 1
        assert body['dishes_count'] == 2

    async def test_get_submenu(self, async_client: AsyncClient):
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
        assert body['dishes_count'] == 2

    async def test_delete_submenu(self, async_client: AsyncClient):
        response = await async_client.delete(
            app.url_path_for(
                'delete_submenu',
                menu_id=self.__class__.menu_id,
                id=self.__class__.submenu_id,
            )
        )
        assert response.status_code == 200

    async def test_get_all_submenus_after_delete(self, async_client: AsyncClient):
        response = await async_client.get(
            app.url_path_for('get_all_submenus', menu_id=self.__class__.menu_id)
        )
        assert response.status_code == 200
        assert response.json() == []

    async def test_get_all_dishes_after_submenu_delete(self, async_client: AsyncClient):
        response = await async_client.get(
            app.url_path_for(
                'get_all_dishes',
                menu_id=self.__class__.menu_id,
                submenu_id=self.__class__.submenu_id,
            )
        )
        assert response.status_code == 200
        assert response.json() == []

    async def test_get_menu_after_submenu_delete(self, async_client: AsyncClient):
        response = await async_client.get(
            app.url_path_for('get_menu', id=self.__class__.menu_id)
        )
        assert response.status_code == 200
        body = response.json()
        assert body['id'] == self.__class__.menu_id
        assert body['submenus_count'] == 0
        assert body['dishes_count'] == 0

    async def test_delete_menu(self, async_client: AsyncClient):
        response = await async_client.delete(
            app.url_path_for('delete_menu', id=self.__class__.menu_id)
        )
        assert response.status_code == 200

    async def test_get_all_menus_after_delete(self, async_client: AsyncClient):
        response = await async_client.get(app.url_path_for('get_all_menus'))
        assert response.status_code == 200
        assert response.json() == []
