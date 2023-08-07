import uuid

from schemas.menu import MenuDTO
from schemas.submenu import SubmenuCreate, SubmenuDTO


class SubmenuServiceMock:
    def __init__(self, menus: list[MenuDTO], submenus: list[SubmenuDTO]):
        self.menus = menus
        self.submenus = submenus

    async def get_all(self, menu_id: uuid.UUID) -> list[SubmenuDTO]:
        return [submenu for submenu in self.submenus if submenu.menu_id == menu_id]

    async def get(self, menu_id: uuid.UUID, id: uuid.UUID) -> SubmenuDTO | None:
        return next(
            (
                submenu
                for submenu in self.submenus
                if submenu.id == id and submenu.menu_id == menu_id
            ),
            None,
        )

    async def create(
        self, menu_id: uuid.UUID, submenu_create: SubmenuCreate
    ) -> SubmenuDTO | None:
        return next(
            (
                SubmenuDTO.model_validate(
                    submenu_create.model_dump()
                    | {'id': uuid.uuid4(), 'menu_id': menu_id, 'dishes_count': 0}
                )
                for menu in self.menus
                if menu.id == menu_id
            ),
            None,
        )

    async def update(
        self, menu_id: uuid.UUID, id: uuid.UUID, submenu_create: SubmenuCreate
    ) -> SubmenuDTO | None:
        return next(
            (
                SubmenuDTO.model_validate(
                    submenu.model_dump() | submenu_create.model_dump()
                )
                for submenu in self.submenus
                if submenu.menu_id == menu_id and submenu.id == id
            ),
            None,
        )

    async def delete(self, menu_id: uuid.UUID, id: uuid.UUID) -> uuid.UUID | None:
        return next(
            (
                submenu.id
                for submenu in self.submenus
                if submenu.id == id and submenu.menu_id == menu_id
            ),
            None,
        )
