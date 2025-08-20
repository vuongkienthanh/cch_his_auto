import time

from selenium.webdriver import Keys

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tracing import _root

_lgr = _root.getChild("search menu")

MENU_CSS = "div:has(>.ant-select~div>div>.ant-select-dropdown)"
MENU_SEARCH_CSS = f"{MENU_CSS} input[type=search]"
MENU_ITEMS_CSS = f"{MENU_CSS} .ant-select-dropdown"


def goto(d: Driver, name: str):
    _lgr.debug(f"filter with name= {name}")
    d.waiting(f"{MENU_ITEMS_CSS} .ant-select-item", "menu item")
    search_bar = d.clear_input(MENU_SEARCH_CSS)
    search_bar.send_keys(name)
    time.sleep(2)
    search_bar.send_keys(Keys.ENTER)
