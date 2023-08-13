import sys

from admin.xl_parser import parse_menus
from background.celery import app

sys.path = ['..', '.'] + sys.path


@app.task(name='update_menus')
def update_menus():
    menus = parse_menus()
    print(menus)
