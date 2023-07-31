from httpx import AsyncClient
from repository.menu import MenuRepository
from schemas.menu import MenuDTO, MenuCreate
from main import app
import uuid
import pytest

pytestmark = pytest.mark.anyio


def setup_module():
    app.dependency_overrides[MenuRepository.create] = create
    app.dependency_overrides[MenuRepository.read_all] = read_all
    app.dependency_overrides[MenuRepository.read] = read
    app.dependency_overrides[MenuRepository.update] = update
    app.dependency_overrides[MenuRepository.delete] = delete


menus = [
    MenuDTO(
        id=uuid.uuid4(),
        title="Menu 1",
        description="Menu 1 description",
        submenus_count=2,
        dishes_count=3,
    ),
    MenuDTO(
        id=uuid.uuid4(),
        title="Menu 2",
        description="Menu 2 description",
        submenus_count=2,
        dishes_count=3,
    ),
]


async def read_all():
    return menus


async def read(id: uuid.UUID):
    return next((menu for menu in menus if menu.id == id), None)


async def create(menu_create: MenuCreate):
    return MenuDTO.model_validate(
        menu_create.model_dump()
        | {"id": uuid.uuid4(), "submenus_count": 0, "dishes_count": 0}
    )


async def update(id: uuid.UUID, menu_create: MenuCreate):
    return next(
        (
            MenuDTO.model_validate(
                menu.model_dump() | menu_create.model_dump()
            )
            for menu in menus
            if menu.id == id
        ),
        None,
    )


async def delete(id: uuid.UUID):
    return next((menu.id for menu in menus if menu.id == id), None)


async def test_get_all(async_client: AsyncClient):
    response = await async_client.get("menus")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_one(async_client: AsyncClient):
    response = await async_client.get(f"menus/{menus[0].id}")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


async def test_get_one_not_found(async_client: AsyncClient):
    response = await async_client.get(f"menus/{uuid.uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "menu not found"


async def test_create(async_client: AsyncClient):
    response = await async_client.post(
        "menus",
        json=MenuCreate(
            title="Menu 3", description="Menu 3 description"
        ).model_dump(mode="json"),
    )
    assert response.status_code == 201
    assert isinstance(response.json(), dict)


async def test_update(async_client: AsyncClient):
    response = await async_client.patch(
        f"menus/{menus[0].id}",
        json=MenuCreate(
            title="Menu 3", description="Menu 3 description"
        ).model_dump(mode="json"),
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


async def test_update_not_found(async_client: AsyncClient):
    response = await async_client.patch(
        f"menus/{uuid.uuid4()}",
        json=MenuCreate(
            title="Menu 3", description="Menu 3 description"
        ).model_dump(mode="json"),
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "menu not found"


async def test_delete(async_client: AsyncClient):
    response = await async_client.delete(f"menus/{menus[0].id}")
    assert response.status_code == 200
    assert isinstance(response.json(), str)


async def test_delete_not_found(async_client: AsyncClient):
    response = await async_client.delete(f"menus/{uuid.uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "menu not found"
