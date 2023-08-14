import logging
from os import getenv

from httpx import AsyncClient

from background.xl_parser.schemas import (
    MenuCascadeCreate,
    XLBindings,
    XLDishBinding,
    XLMenuBinding,
    XLSubmenuBinding,
)
from schemas.dish import DishCreate, DishDTO
from schemas.menu import MenuCreate, MenuDTO
from schemas.submenu import SubmenuCreate, SubmenuDTO

logging.basicConfig(level=logging.INFO)


# TODO refactor this function, split it and avoid code duplication
async def sync_menus(
    menus: list[MenuCascadeCreate],
    bindings_path: str = 'background/xl_parser/cache/bindings.json',
):
    try:
        xl_bindings = XLBindings.model_validate_json(open(bindings_path).read())
    except Exception:
        xl_bindings = XLBindings()
    app_url = getenv('APP_URL')
    base_api_url = f'{app_url}/api/v1/menus'
    for menu in menus:
        menu_api_url = base_api_url
        # logging.info(f'menu: {menu.id}')
        if menu_binding := next(
            (
                menu_binding
                for menu_binding in xl_bindings.menus
                if menu_binding.xl_id == menu.id
            ),
            None,
        ):
            async with AsyncClient() as client:
                if (
                    await client.get(f'{menu_api_url}/{menu_binding.db_id}')
                ).status_code == 404:
                    created_menu = MenuDTO(
                        **(
                            await client.post(
                                menu_api_url,
                                json=MenuCreate(**menu.model_dump()).model_dump(
                                    mode='json'
                                ),
                            )
                        ).json()
                    )
                    menu_binding.db_id = created_menu.id
                    menu_binding.submenus = []
                else:
                    await client.patch(
                        f'{menu_api_url}/{menu_binding.db_id}',
                        json=MenuCreate(**menu.model_dump()).model_dump(mode='json'),
                    )
        else:
            async with AsyncClient() as client:
                created_menu = MenuDTO(
                    **(
                        await client.post(
                            menu_api_url,
                            json=MenuCreate(**menu.model_dump()).model_dump(
                                mode='json'
                            ),
                        )
                    ).json()
                )
            menu_binding = XLMenuBinding(
                xl_id=menu.id,
                db_id=created_menu.id,
            )
            xl_bindings.menus.append(menu_binding)

        submenu_api_url = f'{menu_api_url}/{menu_binding.db_id}/submenus'
        for submenu in menu.submenus:
            # logging.info(f'submenu: {submenu.id}')
            if submenu_binding := next(
                (
                    submenu_binding
                    for submenu_binding in menu_binding.submenus
                    if submenu_binding.xl_id == submenu.id
                ),
                None,
            ):
                async with AsyncClient() as client:
                    await client.patch(
                        f'{submenu_api_url}/{submenu_binding.db_id}',
                        json=SubmenuCreate(**submenu.model_dump()).model_dump(
                            mode='json'
                        ),
                    )
            else:
                async with AsyncClient() as client:
                    created_submenu = SubmenuDTO(
                        **(
                            await client.post(
                                submenu_api_url,
                                json=SubmenuCreate(**submenu.model_dump()).model_dump(
                                    mode='json'
                                ),
                            )
                        ).json()
                    )
                if created_submenu is None:
                    return
                submenu_binding = XLSubmenuBinding(
                    xl_id=submenu.id,
                    db_id=created_submenu.id,
                )
                menu_binding.submenus.append(submenu_binding)

            dish_api_url = f'{submenu_api_url}/{submenu_binding.db_id}/dishes'
            for dish in submenu.dishes:
                # logging.info(f'dish: {dish.id}')
                if dish_binding := next(
                    (
                        dish_binding
                        for dish_binding in submenu_binding.dishes
                        if dish_binding.xl_id == dish.id
                    ),
                    None,
                ):
                    async with AsyncClient() as client:
                        await client.patch(
                            f'{dish_api_url}/{dish_binding.db_id}',
                            json=DishCreate(**dish.model_dump()).model_dump(
                                mode='json'
                            ),
                        )
                else:
                    async with AsyncClient() as client:
                        created_dish = DishDTO(
                            **(
                                await client.post(
                                    dish_api_url,
                                    json=DishCreate(**dish.model_dump()).model_dump(
                                        mode='json'
                                    ),
                                )
                            ).json()
                        )

                    if created_dish is None:
                        return
                    dish_binding = XLDishBinding(
                        xl_id=dish.id,
                        db_id=created_dish.id,
                    )
                    submenu_binding.dishes.append(dish_binding)
    open(bindings_path, 'w').write(xl_bindings.model_dump_json())
