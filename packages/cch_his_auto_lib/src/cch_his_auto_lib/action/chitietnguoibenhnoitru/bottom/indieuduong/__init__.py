import logging
import time

from selenium.webdriver import Keys

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tracing import tracing

_lgr = logging.getLogger("bot_indieuduong")
_trace = tracing(_lgr)


MENU_CSS = "div:has(>.ant-select~div>div>.ant-select-dropdown)"
MENU_SEARCH_CSS = f"{MENU_CSS} input[type=search]"
MENU_ITEMS_CSS = f"{MENU_CSS} .ant-select-dropdown"


@_trace
def goto(d: Driver, name: str):
    "Open *In điều dưỡng*, filter selection based on `name`"
    _lgr.debug(f"indieuduong goto {name}")
    d.clicking(".footer-btn .right button:nth-child(3)", "open In điều dưỡng")
    d.waiting(f"{MENU_ITEMS_CSS} .ant-select-item", "menu item")
    search_bar = d.clear_input(MENU_SEARCH_CSS)
    search_bar.send_keys(name)
    time.sleep(2)
    search_bar.send_keys(Keys.ENTER)


from .bangkechiphiBHYT import sign_bangkechiphiBHYT
from .camketchungvenhapvien import get_signature_data

