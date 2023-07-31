from httpx import AsyncClient
from repository.dish import DishRepository
from schemas.menu import MenuDTO
from schemas.submenu import SubmenuDTO
from schemas.dish import DishDTO, DishCreate
from decimal import Decimal
from main import app
import uuid
import pytest

pytestmark = pytest.mark.anyio


def setup_module():
    app.dependency_overrides[DishRepository.create] = create
    app.dependency_overrides[DishRepository.read_all] = read_all
    app.dependency_overrides[DishRepository.read] = read
    app.dependency_overrides[DishRepository.update] = update
    app.dependency_overrides[DishRepository.delete] = delete


menus = [
    MenuDTO(
        id=uuid.uuid4(),
        title="Menu 1",
        description="Menu 1 description",
        submenus_count=1,
        dishes_count=2,
    ),
]


submenus = [
    SubmenuDTO(
        id=uuid.uuid4(),
        title="Menu 1",
        description="Menu 1 description",
        menu_id=menus[0].id,
        dishes_count=2,
    ),
]


dishes = [
    DishDTO(
        id=uuid.uuid4(),
        title="Dish 1",
        description="Dish 1 description",
        price=Decimal("249.00"),
        submenu_id=submenus[0].id,
    ),
    DishDTO(
        id=uuid.uuid4(),
        title="Dish 2",
        description="Dish 2 description",
        price=Decimal("379.00"),
        submenu_id=submenus[0].id,
    ),
]


async def read_all(menu_id: uuid.UUID, submenu_id: uuid.UUID):
    return [
        dish
        for dish in dishes
        if next(
            (
                submenu.menu_id == menu_id
                for submenu in submenus
                if submenu.id == submenu_id
            ),
            False,
        )
        and dish.submenu_id == submenu_id
        and dish.id == id
    ]


async def read(menu_id: uuid.UUID, submenu_id: uuid.UUID, id: uuid.UUID):
    return next(
        (
            dish
            for dish in dishes
            if next(
                (
                    submenu.menu_id == menu_id
                    for submenu in submenus
                    if submenu.id == submenu_id
                ),
                False,
            )
            and dish.submenu_id == submenu_id
            and dish.id == id
        ),
        None,
    )


async def create(
    menu_id: uuid.UUID, submenu_id: uuid.UUID, submenu_create: DishCreate
):
    return next(
        (
            DishDTO.model_validate(
                submenu_create.model_dump()
                | {"id": uuid.uuid4(), "submenu_id": submenu_id}
            )
            for menu in menus
            if next(
                (
                    submenu.menu_id == menu_id
                    for submenu in submenus
                    if submenu.id == submenu_id
                ),
                False,
            )
            and menu.id == menu_id
        ),
        None,
    )


async def update(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    id: uuid.UUID,
    dish_create: DishCreate,
):
    return next(
        (
            DishDTO.model_validate(
                dish.model_dump() | dish_create.model_dump()
            )
            for dish in dishes
            if next(
                (
                    submenu.menu_id == menu_id
                    for submenu in submenus
                    if submenu.id == submenu_id
                ),
                False,
            )
            and dish.submenu_id == submenu_id
            and dish.id == id
        ),
        None,
    )


async def delete(menu_id: uuid.UUID, submenu_id: uuid.UUID, id: uuid.UUID):
    return next(
        (
            dish.id
            for dish in dishes
            if next(
                (
                    submenu.menu_id == menu_id
                    for submenu in submenus
                    if submenu.id == submenu_id
                ),
                False,
            )
            and dish.submenu_id == submenu_id
            and dish.id == id
        ),
        None,
    )


async def test_get_all(async_client: AsyncClient):
    response = await async_client.get(
        f"menus/{menus[0].id}/submenus/{submenus[0].id}/dishes"
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_one(async_client: AsyncClient):
    response = await async_client.get(
        f"menus/{menus[0].id}/submenus/{submenus[0].id}/dishes/{dishes[0].id}"
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


async def test_get_one_not_found(async_client: AsyncClient):
    response = await async_client.get(
        f"menus/{menus[0].id}/submenus/{submenus[0].id}/dishes/{uuid.uuid4()}"
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "dish not found"


async def test_create(async_client: AsyncClient):
    response = await async_client.post(
        f"menus/{menus[0].id}/submenus/{submenus[0].id}/dishes",
        json=DishCreate(
            title="Dish 3",
            description="Dish 3 description",
            price=Decimal("149.00"),
        ).model_dump(mode="json"),
    )
    assert response.status_code == 201
    assert isinstance(response.json(), dict)


async def test_update(async_client: AsyncClient):
    response = await async_client.patch(
        f"menus/{menus[0].id}/submenus/{submenus[0].id}/dishes/{dishes[0].id}",
        json=DishCreate(
            title="Dish 3",
            description="Dish 3 description",
            price=Decimal("149.00"),
        ).model_dump(mode="json"),
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


async def test_update_not_found(async_client: AsyncClient):
    response = await async_client.patch(
        f"menus/{menus[0].id}/submenus/{submenus[0].id}/dishes/{uuid.uuid4()}",
        json=DishCreate(
            title="Dish 3",
            description="Dish 3 description",
            price=Decimal("149.00"),
        ).model_dump(mode="json"),
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "dish not found"


async def test_delete(async_client: AsyncClient):
    response = await async_client.delete(
        f"menus/{menus[0].id}/submenus/{submenus[0].id}/dishes/{dishes[0].id}"
    )
    assert response.status_code == 200
    assert isinstance(response.json(), str)


async def test_delete_not_found(async_client: AsyncClient):
    response = await async_client.delete(
        f"menus/{menus[0].id}/submenus/{submenus[0].id}/dishes/{uuid.uuid4()}"
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "dish not found"
