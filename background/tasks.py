import asyncio

from background.celery import app
from background.xl_parser.db_sync import sync_menus
from background.xl_parser.xl_parser import parse_menus

loop = asyncio.new_event_loop()


@app.task(name='update_menus')
def update_menus():
    loop.run_until_complete(
        sync_menus(parse_menus(), 'background/xl_parser/cache/bindings.json')
    )
