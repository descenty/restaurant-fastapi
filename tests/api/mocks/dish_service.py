import uuid

from schemas.dish import DishCreate, DishDTO
from schemas.menu import MenuDTO
from schemas.submenu import SubmenuDTO


class DishServiceMock:
    def __init__(
        self, menus: list[MenuDTO], submenus: list[SubmenuDTO], dishes: list[DishDTO]
    ):
        self.menus = menus
        self.submenus = submenus
        self.dishes = dishes

    async def get_all(self, menu_id: uuid.UUID, submenu_id: uuid.UUID) -> list[DishDTO]:
        print(self.dishes)
        return [
            dish
            for dish in self.dishes
            if next(
                (
                    submenu.menu_id == menu_id
                    for submenu in self.submenus
                    if submenu.id == submenu_id
                ),
                False,
            )
            and dish.submenu_id == submenu_id
            and dish.id == id
        ]

    async def get(
        self, menu_id: uuid.UUID, submenu_id: uuid.UUID, id: uuid.UUID
    ) -> DishDTO | None:
        return next(
            (
                dish
                for dish in self.dishes
                if next(
                    (
                        submenu.menu_id == menu_id
                        for submenu in self.submenus
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
        self,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        submenu_create: DishCreate,
    ) -> DishDTO | None:
        return next(
            (
                DishDTO.model_validate(
                    submenu_create.model_dump()
                    | {'id': uuid.uuid4(), 'submenu_id': submenu_id}
                )
                for menu in self.menus
                if next(
                    (
                        submenu.menu_id == menu_id
                        for submenu in self.submenus
                        if submenu.id == submenu_id
                    ),
                    False,
                )
                and menu.id == menu_id
            ),
            None,
        )

    async def update(
        self,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        id: uuid.UUID,
        dish_create: DishCreate,
    ) -> DishDTO | None:
        return next(
            (
                DishDTO.model_validate(dish.model_dump() | dish_create.model_dump())
                for dish in self.dishes
                if next(
                    (
                        submenu.menu_id == menu_id
                        for submenu in self.submenus
                        if submenu.id == submenu_id
                    ),
                    False,
                )
                and dish.submenu_id == submenu_id
                and dish.id == id
            ),
            None,
        )

    async def delete(
        self, menu_id: uuid.UUID, submenu_id: uuid.UUID, id: uuid.UUID
    ) -> uuid.UUID | None:
        return next(
            (
                dish.id
                for dish in self.dishes
                if next(
                    (
                        submenu.menu_id == menu_id
                        for submenu in self.submenus
                        if submenu.id == submenu_id
                    ),
                    False,
                )
                and dish.submenu_id == submenu_id
                and dish.id == id
            ),
            None,
        )
