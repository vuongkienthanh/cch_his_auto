import time

from selenium.webdriver import Keys
from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tracing import _root_lgr

URL = "http://emr.ndtp.org/quan-ly-noi-tru/chi-tiet-nguoi-benh-noi-tru/"

_lgr = _root_lgr.getChild("chitietnguoibenhnoitru")


MAIN_CSS = "#root .content"
NAV_CSS = f"{MAIN_CSS} .ant-tabs-nav-list"
ACTIVE_PANE = f"{MAIN_CSS} .ant-tabs-tabpane-active"


def is_tab_active(d: Driver, tab: int) -> bool:
    try:
        d.waiting(f"#rc-tabs-0-panel-{tab}.ant-tabs-tabpane-active")
        return True
    except NoSuchElementException:
        return False


def change_tab(d: Driver, tab: int):
    d.clicking(f"{NAV_CSS}>div[data-node-key='{tab}']")
    assert is_tab_active(d, tab)


MENU_CSS = "div:has(>.ant-select~div>div>.ant-select-dropdown)"
MENU_SEARCH_CSS = f"{MENU_CSS} input[type=search]"
MENU_ITEMS_CSS = f"{MENU_CSS} .ant-select-dropdown"


def _click_menu_item(d: Driver, name: str):
    search_bar = d.clear_input(MENU_SEARCH_CSS)
    search_bar.send_keys(name)
    time.sleep(2)
    search_bar.send_keys(Keys.ENTER)


def click_inbacsi(d: Driver, name:str):
    "Open *In bác sĩ*, filter selection based on `name`"
    d.clicking(".footer-btn .right button:nth-child(2)")
    d.waiting(f"{MENU_ITEMS_CSS} .ant-select-item")
    _click_menu_item(d, name)


def click_indieuduong(d: Driver, name:str):
    "Open *In điều dưỡng*, filter selection based on `name`"
    d.clicking(".footer-btn .right button:nth-child(3)")
    d.waiting(f"{MENU_ITEMS_CSS} .ant-select-item")
    _click_menu_item(d, name)
