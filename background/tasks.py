import asyncio
import sys

from background.celery import app
from background.xl_parser.db_sync import sync_menus
from background.xl_parser.xl_parser import parse_menus
from core.config import settings

sys.path = ['..', '.'] + sys.path

loop = asyncio.get_event_loop()


@app.task(name='update_menus')
def update_menus():
    settings.redis.enabled = False
    loop.run_until_complete(
        sync_menus(parse_menus(), 'background/xl_parser/cache/bindings.json')
    )
