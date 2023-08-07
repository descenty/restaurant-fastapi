import uuid

from schemas.menu import MenuCreate, MenuDTO


class MenuServiceMock:
    def __init__(self, menus: list[MenuDTO] = []):
        self.menus = menus

    async def get_all(
        self,
    ) -> list[MenuDTO]:
        return self.menus

    async def get(self, id: uuid.UUID) -> MenuDTO | None:
        return next((menu for menu in self.menus if menu.id == id), None)

    async def create(self, menu_create: MenuCreate) -> MenuDTO:
        return MenuDTO.model_validate(
            menu_create.model_dump()
            | {'id': uuid.uuid4(), 'submenus_count': 0, 'dishes_count': 0}
        )

    async def update(self, id: uuid.UUID, menu_create: MenuCreate) -> MenuDTO | None:
        return next(
            (
                MenuDTO.model_validate(menu.model_dump() | menu_create.model_dump())
                for menu in self.menus
                if menu.id == id
            ),
            None,
        )

    async def delete(self, id: uuid.UUID) -> uuid.UUID | None:
        return next((menu.id for menu in self.menus if menu.id == id), None)
