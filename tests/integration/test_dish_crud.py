import pytest
from httpx import AsyncClient

from main import app

pytestmark = pytest.mark.anyio


class TestDishCRUD:
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

    async def test_create_submenu(self, async_client):
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

    async def test_get_all(self, async_client: AsyncClient):
        response = await async_client.get(
            app.url_path_for(
                'get_all_dishes',
                menu_id=self.__class__.menu_id,
                submenu_id=self.__class__.submenu_id,
            ),
        )
        assert response.status_code == 200
        assert response.json() == []

    async def test_create(self, async_client):
        response = await async_client.post(
            app.url_path_for(
                'create_dish',
                menu_id=self.__class__.menu_id,
                submenu_id=self.__class__.submenu_id,
            ),
            json={
                'title': 'My dish 1',
                'description': 'My dish description 1',
                'price': '12.50',
            },
        )
        assert response.status_code == 201
        body = response.json()
        self.__class__.dish_id = body['id']
        self.__class__.dish_title = body['title']
        self.__class__.dish_description = body['description']
        self.__class__.dish_price = body['price']
        assert body['id'] == self.__class__.dish_id
        assert body['title'] == self.__class__.dish_title
        assert body['description'] == self.__class__.dish_description
        assert body['price'] == self.__class__.dish_price

    async def test_get_all_after_create(self, async_client: AsyncClient):
        response = await async_client.get(
            app.url_path_for(
                'get_all_dishes',
                menu_id=self.__class__.menu_id,
                submenu_id=self.__class__.submenu_id,
            )
        )
        assert response.status_code == 200
        assert response.json() != []

    async def test_get(self, async_client: AsyncClient):
        response = await async_client.get(
            app.url_path_for(
                'get_dish',
                menu_id=self.__class__.menu_id,
                submenu_id=self.__class__.submenu_id,
                id=self.__class__.dish_id,
            )
        )
        assert response.status_code == 200
        body = response.json()
        assert body['id'] == self.__class__.dish_id
        assert body['title'] == self.__class__.dish_title
        assert body['description'] == self.__class__.dish_description
        assert body['price'] == self.__class__.dish_price

    async def test_update(self, async_client: AsyncClient):
        response = await async_client.patch(
            app.url_path_for(
                'update_dish',
                menu_id=self.__class__.menu_id,
                submenu_id=self.__class__.submenu_id,
                id=self.__class__.dish_id,
            ),
            json={
                'title': 'My updated dish 1',
                'description': 'My updated dish description 1',
                'price': '14.50',
            },
        )
        assert response.status_code == 200
        body = response.json()
        assert body['title'] != self.__class__.dish_title
        assert body['description'] != self.__class__.dish_description
        assert body['price'] != self.__class__.dish_price
        self.__class__.dish_title = body['title']
        self.__class__.dish_description = body['description']
        self.__class__.dish_price = body['price']
        assert body['title'] == self.__class__.dish_title
        assert body['description'] == self.__class__.dish_description
        assert body['price'] == self.__class__.dish_price

    async def test_get_after_update(self, async_client: AsyncClient):
        response = await async_client.get(
            app.url_path_for(
                'get_dish',
                menu_id=self.__class__.menu_id,
                submenu_id=self.__class__.submenu_id,
                id=self.__class__.dish_id,
            )
        )
        assert response.status_code == 200
        body = response.json()
        assert body['id'] == self.__class__.dish_id
        assert body['title'] == self.__class__.dish_title
        assert body['description'] == self.__class__.dish_description
        assert body['price'] == self.__class__.dish_price

    async def test_delete(self, async_client: AsyncClient):
        response = await async_client.delete(
            app.url_path_for(
                'delete_dish',
                menu_id=self.__class__.menu_id,
                submenu_id=self.__class__.submenu_id,
                id=self.__class__.dish_id,
            )
        )
        assert response.status_code == 200

    async def test_get_all_after_delete(self, async_client: AsyncClient):
        response = await async_client.get(
            app.url_path_for(
                'get_all_dishes',
                menu_id=self.__class__.menu_id,
                submenu_id=self.__class__.submenu_id,
            )
        )
        assert response.status_code == 200
        assert response.json() == []

    async def test_get_after_delete(self, async_client: AsyncClient):
        response = await async_client.get(
            app.url_path_for(
                'get_dish',
                menu_id=self.__class__.menu_id,
                submenu_id=self.__class__.submenu_id,
                id=self.__class__.dish_id,
            )
        )
        assert response.status_code == 404
        assert response.json()['detail'] == 'dish not found'

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

    async def test_delete_menu(self, async_client: AsyncClient):
        response = await async_client.delete(
            app.url_path_for('delete_menu', id=self.__class__.menu_id)
        )
        assert response.status_code == 200

    async def test_get_all_menus_after_delete(self, async_client: AsyncClient):
        response = await async_client.get(app.url_path_for('get_all_menus'))
        assert response.status_code == 200
        assert response.json() == []
