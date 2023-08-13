from decimal import Decimal

import pytest
from httpx import AsyncClient

from main import app
from schemas.dish import DishCreate, DishDTO
from schemas.menu import MenuCascadeDTO, MenuCreate
from schemas.submenu import SubmenuCascadeDTO, SubmenuCreate

pytestmark = pytest.mark.anyio

menus_create: list[MenuCreate] = [
    MenuCreate(title='My menu 1', description='My menu description 1'),
]

submenus_create: list[SubmenuCreate] = [
    SubmenuCreate(title='My submenu 1', description='My submenu description 1'),
]

dishes_create: list[DishCreate] = [
    DishCreate(
        title='My dish 1', description='My dish description 1', price=Decimal('350.0')
    ),
]


class TestMenuCascade:
    menus: list[MenuCascadeDTO] = []

    async def test_get_all_cascade_empty(self, async_client: AsyncClient):
        response = await async_client.get(app.url_path_for('get_all_menus_cascade'))
        assert response.status_code == 200
        assert response.json() == []

    async def test_create_all(self, async_client: AsyncClient):
        for menu in menus_create:
            response = await async_client.post(
                app.url_path_for('create_menu'),
                json=menu.model_dump(mode='json'),
            )
            assert response.status_code == 201
            body = response.json()
            self.menus.append(MenuCascadeDTO(**body))

        for submenu in submenus_create:
            response = await async_client.post(
                app.url_path_for(
                    'create_submenu',
                    menu_id=self.menus[0].id,
                ),
                json=submenu.model_dump(mode='json'),
            )
            assert response.status_code == 201
            body = response.json()
            self.menus[0].submenus.append(SubmenuCascadeDTO(**body))
            self.menus[0].submenus_count += 1

        for dish in dishes_create:
            response = await async_client.post(
                app.url_path_for(
                    'create_dish',
                    menu_id=self.menus[0].id,
                    submenu_id=self.menus[0].submenus[0].id,
                ),
                json=dish.model_dump(mode='json'),
            )
            assert response.status_code == 201
            body = response.json()
            self.menus[0].submenus[0].dishes.append(DishDTO(**body))
            self.menus[0].dishes_count += 1
            self.menus[0].submenus[0].dishes_count += 1

    async def test_get_all_cascade(self, async_client: AsyncClient):
        response = await async_client.get(app.url_path_for('get_all_menus_cascade'))
        assert response.status_code == 200
        menus = [MenuCascadeDTO.model_validate(menu) for menu in response.json()]
        assert menus[0].id == self.menus[0].id
        assert menus[0].submenus[0].id == self.menus[0].submenus[0].id
        assert (
            menus[0].submenus[0].dishes[0].id == self.menus[0].submenus[0].dishes[0].id
        )

    async def test_delete_all(self, async_client: AsyncClient):
        for menu in self.menus:
            response = await async_client.delete(
                app.url_path_for('delete_menu', id=menu.id)
            )
            assert response.status_code == 200
            assert response.json() == str(menu.id)

    async def test_get_all_cascade_clear(self, async_client: AsyncClient):
        response = await async_client.get(app.url_path_for('get_all_menus_cascade'))
        assert response.status_code == 200
        assert response.json() == []
