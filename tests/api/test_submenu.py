# import pytest
# from .client import get_async_client, app
# from repository.submenu import SubmenuRepository
# from schemas.submenu import SubmenuDTO, SubmenuCreate
# import uuid

# pytestmark = pytest.mark.anyio

# submenus = [
#     SubmenuDTO(
#         id=uuid.uuid4(),
#         title="Menu 1",
#         description="Menu 1 description",
        
#     ),
#     SubmenuDTO(
#         id=uuid.uuid4(),
#         title="Menu 2",
#         description="Menu 2 description",
#         submenus_count=2,
#         dishes_count=3,
#     ),
# ]


# async def read_all():
#     return menus


# async def read(id: uuid.UUID):
#     return next((menu for menu in menus if menu.id == id), None)


# async def create(menu: MenuCreate):
#     return MenuDTO.model_validate(
#         menu.model_dump()
#         | {"id": uuid.uuid4(), "submenus_count": 0, "dishes_count": 0}
#     )


# async def update(id: uuid.UUID, menu: MenuCreate):
#     return (
#         MenuDTO.model_validate(
#             menu.model_dump()
#             | {"id": id, "submenus_count": 0, "dishes_count": 0}
#         )
#         if id in [menu.id for menu in menus]
#         else None
#     )


# async def delete(id: uuid.UUID):
#     return id if id in [menu.id for menu in menus] else None


# app.dependency_overrides[MenuRepository.create] = create
# app.dependency_overrides[MenuRepository.read_all] = read_all
# app.dependency_overrides[MenuRepository.read] = read
# app.dependency_overrides[MenuRepository.update] = update
# app.dependency_overrides[MenuRepository.delete] = delete


# async def test_get_all():
#     async with get_async_client() as ac:
#         response = await ac.get("menus")
#     assert response.status_code == 200
#     assert len(response.json()) == len(menus)


# async def test_get_one():
#     async with get_async_client() as ac:
#         response = await ac.get(f"menus/{menus[0].id}")
#     assert response.status_code == 200
#     assert MenuDTO.model_validate(response.json()) == menus[0]


# async def test_get_one_not_found():
#     async with get_async_client() as ac:
#         response = await ac.get(f"menus/{uuid.uuid4()}")
#     assert response.status_code == 404


# async def test_create():
#     async with get_async_client() as ac:
#         response = await ac.post(
#             "menus",
#             json=MenuCreate(
#                 title="Menu 3", description="Menu 3 description"
#             ).model_dump(),
#         )
#     assert response.status_code == 201
#     assert response.json()["title"] == "Menu 3"


# async def test_update():
#     async with get_async_client() as ac:
#         response = await ac.patch(
#             f"menus/{menus[0].id}",
#             json=MenuCreate(
#                 title="Menu 3", description="Menu 3 description"
#             ).model_dump(),
#         )
#     assert response.status_code == 200
#     assert response.json()["title"] == "Menu 3"


# async def test_update_not_found():
#     async with get_async_client() as ac:
#         response = await ac.patch(
#             f"menus/{uuid.uuid4()}",
#             json=MenuCreate(
#                 title="Menu 3", description="Menu 3 description"
#             ).model_dump(),
#         )
#     assert response.status_code == 404


# async def test_delete():
#     async with get_async_client() as ac:
#         response = await ac.delete(f"menus/{menus[0].id}")
#     assert response.status_code == 200
#     assert response.json() == str(menus[0].id)


# async def test_delete_not_found():
#     async with get_async_client() as ac:
#         response = await ac.delete(f"menus/{uuid.uuid4()}")
#     assert response.status_code == 404
