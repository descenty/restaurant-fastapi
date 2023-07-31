from httpx import AsyncClient
import pytest

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
            "menus",
            json={
                "title": "My menu 1",
                "description": "My menu description 1",
            },
        )
        assert response.status_code == 201
        body = response.json()
        self.__class__.menu_id = body["id"]
        assert body["id"] == self.__class__.menu_id

    async def test_get_all(self, async_client: AsyncClient):
        response = await async_client.get(
            f"menus/{self.__class__.menu_id}/submenus"
        )
        assert response.status_code == 200
        assert response.json() == []

    async def test_create(self, async_client):
        response = await async_client.post(
            f"menus/{self.__class__.menu_id}/submenus",
            json={
                "title": "My submenu 1",
                "description": "My submenu description 1",
            },
        )
        assert response.status_code == 201
        body = response.json()
        self.__class__.submenu_id = body["id"]
        self.__class__.submenu_title = body["title"]
        self.__class__.submenu_description = body["description"]
        assert body["id"] == self.__class__.submenu_id
        assert body["title"] == self.__class__.submenu_title
        assert body["description"] == self.__class__.submenu_description

    async def test_get_all_after_create(self, async_client: AsyncClient):
        response = await async_client.get(
            f"menus/{self.__class__.menu_id}/submenus"
        )
        assert response.status_code == 200
        assert response.json() != []

    async def test_get(self, async_client: AsyncClient):
        response = await async_client.get(
            f"menus/{self.__class__.menu_id}/submenus/{self.__class__.submenu_id}"
        )
        assert response.status_code == 200
        body = response.json()
        assert body["id"] == self.__class__.submenu_id
        assert body["title"] == self.__class__.submenu_title
        assert body["description"] == self.__class__.submenu_description

    async def test_update(self, async_client: AsyncClient):
        response = await async_client.patch(
            f"menus/{self.__class__.menu_id}/submenus/{self.__class__.submenu_id}",
            json={
                "title": "My updated submenu 1",
                "description": "My updated submenu description 1",
            },
        )
        assert response.status_code == 200
        body = response.json()
        assert body["title"] != self.__class__.submenu_title
        assert body["description"] != self.__class__.submenu_description
        self.__class__.submenu_title = body["title"]
        self.__class__.submenu_description = body["description"]
        assert body["title"] == self.__class__.submenu_title
        assert body["description"] == self.__class__.submenu_description

    async def test_get_after_update(self, async_client: AsyncClient):
        response = await async_client.get(
            f"menus/{self.__class__.menu_id}/submenus/{self.__class__.submenu_id}"
        )
        assert response.status_code == 200
        body = response.json()
        assert body["id"] == self.__class__.submenu_id
        assert body["title"] == self.__class__.submenu_title
        assert body["description"] == self.__class__.submenu_description

    async def test_delete(self, async_client: AsyncClient):
        response = await async_client.delete(
            f"menus/{self.__class__.menu_id}/submenus/{self.__class__.submenu_id}"
        )
        assert response.status_code == 200

    async def test_get_all_after_delete(self, async_client: AsyncClient):
        response = await async_client.get(
            f"menus/{self.__class__.menu_id}/submenus"
        )
        assert response.status_code == 200
        assert response.json() == []

    async def test_get_after_delete(self, async_client: AsyncClient):
        response = await async_client.get(
            f"menus/{self.__class__.menu_id}/submenus/{self.__class__.submenu_id}"
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "submenu not found"

    async def test_delete_menu(self, async_client: AsyncClient):
        response = await async_client.delete(f"menus/{self.__class__.menu_id}")
        assert response.status_code == 200

    async def test_get_all_menus_after_delete(self, async_client: AsyncClient):
        response = await async_client.get("menus")
        assert response.status_code == 200
        assert response.json() == []
