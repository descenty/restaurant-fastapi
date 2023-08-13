import sys

from xl_parser import fetch_menus

sys.path = ['..', '.'] + sys.path


print([menu.model_dump_json() for menu in fetch_menus()])
