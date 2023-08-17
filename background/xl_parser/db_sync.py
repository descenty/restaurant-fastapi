import logging
from typing import cast
from uuid import UUID

import aiofiles  # type: ignore[import]
from httpx import AsyncClient, Response
from pydantic import BaseModel

from background.xl_parser.schemas import (
    DishCascadeCreate,
    IDModel,
    MenuCascadeCreate,
    SubmenuCascadeCreate,
    XLBinding,
    XLMenuBinding,
    XLMenusBindings,
    XLSubmenuBinding,
)
from core.config import settings
from schemas.dish import DishCreate
from schemas.menu import MenuCreate
from schemas.submenu import SubmenuCreate

logging.basicConfig(level=logging.INFO)


async def create_entity(
    api_url: str,
    json: dict,
) -> UUID:
    async with AsyncClient() as client:
        return UUID(
            (
                await client.post(
                    api_url,
                    json=json,
                )
            ).json()['id']
        )


async def update_entity(
    api_url: str,
    entity_id: UUID,
    json: dict,
) -> Response:
    async with AsyncClient() as client:
        return await client.patch(
            f'{api_url}/{entity_id}',
            json=json,
        )


def get_binding(
    bindings: list[XLBinding],
    xl_id: int,
) -> XLBinding | None:
    return next((binding for binding in bindings if binding.xl_id == xl_id), None)


async def create_or_update_entity(
    api_url: str,
    bindings: list[XLBinding] | list[XLMenuBinding] | list[XLSubmenuBinding],
    model: IDModel,
    TargetModel: type[BaseModel],
    TargetBinding: type[XLBinding] | type[XLMenuBinding] | type[XLSubmenuBinding],
) -> XLBinding | XLMenuBinding | XLSubmenuBinding:
    bindings = cast(list[XLBinding], bindings)
    model_json = TargetModel(**model.model_dump()).model_dump(mode='json')
    if binding := get_binding(cast(list[XLBinding], bindings), model.id):
        if (await update_entity(api_url, binding.db_id, model_json)).status_code != 200:
            binding.db_id = await create_entity(api_url, model_json)
    else:
        bindings.append(
            binding := TargetBinding(
                xl_id=model.id, db_id=await create_entity(api_url, model_json)
            )
        )
    return binding


async def sync_removed(
    api_url: str,
    bindings: list[XLBinding] | list[XLMenuBinding] | list[XLSubmenuBinding],
    models: list[MenuCascadeCreate]
    | list[SubmenuCascadeCreate]
    | list[DishCascadeCreate],
):
    bindings = cast(list[XLBinding], bindings)
    for binding in bindings:
        if not next((model for model in models if model.id == binding.xl_id), None):
            async with AsyncClient() as client:
                await client.delete(f'{api_url}/{binding.db_id}')
            bindings.remove(binding)


async def sync_menus(
    menus: list[MenuCascadeCreate],
    bindings_path: str = 'background/xl_parser/cache/bindings.json',
):
    try:
        async with aiofiles.open(bindings_path, 'r') as f:
            menus_bindings = XLMenusBindings.model_validate_json(await f.read())
    except Exception:
        menus_bindings = XLMenusBindings()
    base_api_url = f'{settings.app_url}/api/v1/menus'
    await sync_removed(
        base_api_url,
        menus_bindings.menus,
        menus,
    )
    for menu in menus:
        logging.info(f'menu: {menu.id}')
        menu_binding = cast(
            XLMenuBinding,
            await create_or_update_entity(
                base_api_url,
                menus_bindings.menus,
                menu,
                MenuCreate,
                XLMenuBinding,
            ),
        )
        submenu_api_url = f'{base_api_url}/{menu_binding.db_id}/submenus'
        await sync_removed(
            base_api_url,
            menu_binding.submenus,
            menu.submenus,
        )
        for submenu in menu.submenus:
            logging.info(f'submenu: {submenu.id}')
            submenu_binding = cast(
                XLSubmenuBinding,
                await create_or_update_entity(
                    submenu_api_url,
                    menu_binding.submenus,
                    submenu,
                    SubmenuCreate,
                    XLSubmenuBinding,
                ),
            )
            await sync_removed(
                base_api_url,
                submenu_binding.dishes,
                submenu.dishes,
            )
            dish_api_url = f'{submenu_api_url}/{submenu_binding.db_id}/dishes'
            for dish in submenu.dishes:
                logging.info(f'dish: {dish.id}')
                await create_or_update_entity(
                    dish_api_url,
                    submenu_binding.dishes,
                    dish,
                    DishCreate,
                    XLBinding,
                )

    async with aiofiles.open(bindings_path, 'w') as f:
        await f.write(menus_bindings.model_dump_json())
