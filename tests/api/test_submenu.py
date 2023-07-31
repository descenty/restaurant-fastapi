from httpx import AsyncClient
from schemas.menu import MenuDTO
from repository.submenu import SubmenuRepository
from schemas.submenu import SubmenuDTO, SubmenuCreate
from main import app
import uuid
import pytest

pytestmark = pytest.mark.anyio


def setup_module():
    app.dependency_overrides[SubmenuRepository.create] = create
    app.dependency_overrides[SubmenuRepository.read_all] = read_all
    app.dependency_overrides[SubmenuRepository.read] = read
    app.dependency_overrides[SubmenuRepository.update] = update
    app.dependency_overrides[SubmenuRepository.delete] = delete


menus = [
    MenuDTO(
        id=uuid.uuid4(),
        title="Menu 1",
        description="Menu 1 description",
        submenus_count=2,
        dishes_count=4,
    ),
]


submenus = [
    SubmenuDTO(
        id=uuid.uuid4(),
        title="Menu 1",
        description="Menu 1 description",
        menu_id=menus[0].id,
        dishes_count=3,
    ),
    SubmenuDTO(
        id=uuid.uuid4(),
        title="Menu 2",
        description="Menu 2 description",
        menu_id=menus[0].id,
        dishes_count=1,
    ),
]


async def read_all(menu_id: uuid.UUID):
    return [submenu for submenu in submenus if submenu.menu_id == menu_id]


async def read(menu_id: uuid.UUID, id: uuid.UUID):
    return next(
        (
            submenu
            for submenu in submenus
            if submenu.id == id and submenu.menu_id == menu_id
        ),
        None,
    )


async def create(menu_id: uuid.UUID, submenu_create: SubmenuCreate):
    return next(
        (
            SubmenuDTO.model_validate(
                submenu_create.model_dump()
                | {"id": uuid.uuid4(), "menu_id": menu_id, "dishes_count": 0}
            )
            for menu in menus
            if menu.id == menu_id
        ),
        None,
    )


async def update(
    menu_id: uuid.UUID, id: uuid.UUID, submenu_create: SubmenuCreate
):
    return next(
        (
            SubmenuDTO.model_validate(
                submenu.model_dump() | submenu_create.model_dump()
            )
            for submenu in submenus
            if submenu.menu_id == menu_id and submenu.id == id
        ),
        None,
    )


async def delete(menu_id: uuid.UUID, id: uuid.UUID):
    return next(
        (
            submenu.id
            for submenu in submenus
            if submenu.id == id and submenu.menu_id == menu_id
        ),
        None,
    )


async def test_get_all(async_client: AsyncClient):
    response = await async_client.get(f"menus/{menus[0].id}/submenus")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_one(async_client: AsyncClient):
    response = await async_client.get(
        f"menus/{menus[0].id}/submenus/{submenus[0].id}"
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


async def test_get_one_not_found(async_client: AsyncClient):
    response = await async_client.get(
        f"menus/{menus[0].id}/submenus/{uuid.uuid4()}"
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "submenu not found"


async def test_create(async_client: AsyncClient):
    response = await async_client.post(
        f"menus/{menus[0].id}/submenus",
        json=SubmenuCreate(
            title="Submenu 3", description="Submenu 3 description"
        ).model_dump(mode="json"),
    )
    assert response.status_code == 201
    assert isinstance(response.json(), dict)


async def test_update(async_client: AsyncClient):
    response = await async_client.patch(
        f"menus/{menus[0].id}/submenus/{submenus[0].id}",
        json=SubmenuCreate(
            title="Submenu 3", description="Submenu 3 description"
        ).model_dump(mode="json"),
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


async def test_update_not_found(async_client: AsyncClient):
    response = await async_client.patch(
        f"menus/{menus[0].id}/submenus/{uuid.uuid4()}",
        json=SubmenuCreate(
            title="Submenu 3", description="Submenu 3 description"
        ).model_dump(mode="json"),
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "submenu not found"


async def test_delete(async_client: AsyncClient):
    response = await async_client.delete(
        f"menus/{menus[0].id}/submenus/{submenus[0].id}"
    )
    assert response.status_code == 200
    assert isinstance(response.json(), str)


async def test_delete_not_found(async_client: AsyncClient):
    response = await async_client.delete(
        f"menus/{menus[0].id}/submenus/{uuid.uuid4()}"
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "submenu not found"
