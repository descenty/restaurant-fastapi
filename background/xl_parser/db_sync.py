import logging

from fastapi import BackgroundTasks

from background.xl_parser.schemas import (
    MenuCascadeCreate,
    XLBindings,
    XLDishBinding,
    XLMenuBinding,
    XLSubmenuBinding,
)
from repositories.dish_repository import DishRepository
from repositories.menu_repository import MenuRepository
from repositories.submenu_repository import SubmenuRepository
from schemas.dish import DishCreate
from schemas.menu import MenuCreate
from schemas.submenu import SubmenuCreate
from services.dish_service import DishService
from services.menu_service import MenuService
from services.submenu_service import SubmenuService

logging.basicConfig(level=logging.INFO)


async def sync_menus(
    menus: list[MenuCascadeCreate],
    bindings_path: str = 'background/xl_parser/cache/bindings.json',
):
    try:
        xl_bindings = XLBindings.model_validate_json(open(bindings_path).read())
    except Exception:
        xl_bindings = XLBindings()
    menu_service = MenuService(MenuRepository(BackgroundTasks()))
    submenu_service = SubmenuService(SubmenuRepository(BackgroundTasks()))
    dish_service = DishService(DishRepository(BackgroundTasks()))
    for menu in menus:
        logging.info(f'menu: {menu.id}')
        if menu_binding := next(
            (
                menu_binding
                for menu_binding in xl_bindings.menus
                if menu_binding.xl_id == menu.id
            ),
            None,
        ):
            await menu_service.update(
                menu_binding.db_id, MenuCreate(**menu.model_dump())
            )
        else:
            menu_binding = XLMenuBinding(
                xl_id=menu.id,
                db_id=(await menu_service.create(MenuCreate(**menu.model_dump()))).id,
            )
            xl_bindings.menus.append(menu_binding)

        for submenu in menu.submenus:
            logging.info(f'submenu: {submenu.id}')
            if submenu_binding := next(
                (
                    submenu_binding
                    for submenu_binding in menu_binding.submenus
                    if submenu_binding.xl_id == submenu.id
                ),
                None,
            ):
                await submenu_service.update(
                    menu_binding.db_id,
                    submenu_binding.db_id,
                    SubmenuCreate(**submenu.model_dump()),
                )
            else:
                if (
                    created_submenu := await submenu_service.create(
                        menu_binding.db_id, SubmenuCreate(**submenu.model_dump())
                    )
                ) is None:
                    return
                submenu_binding = XLSubmenuBinding(
                    xl_id=submenu.id,
                    db_id=created_submenu.id,
                )
                menu_binding.submenus.append(submenu_binding)

            for dish in submenu.dishes:
                logging.info(f'dish: {dish.id}')
                if dish_binding := next(
                    (
                        dish_binding
                        for dish_binding in submenu_binding.dishes
                        if dish_binding.xl_id == dish.id
                    ),
                    None,
                ):
                    await dish_service.update(
                        menu_binding.db_id,
                        submenu_binding.db_id,
                        dish_binding.db_id,
                        DishCreate(**dish.model_dump()),
                    )
                else:
                    if (
                        created_dish := await dish_service.create(
                            menu_binding.db_id,
                            submenu_binding.db_id,
                            DishCreate(**dish.model_dump()),
                        )
                    ) is None:
                        return
                    dish_binding = XLDishBinding(
                        xl_id=dish.id,
                        db_id=created_dish.id,
                    )
                    submenu_binding.dishes.append(dish_binding)
    open(bindings_path, 'w').write(xl_bindings.model_dump_json())
