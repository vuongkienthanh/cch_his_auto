from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import Driver

from .. import _lgr

MAIN_CSS = "#root .content"
NAV_CSS = f"{MAIN_CSS} .ant-tabs-nav-list"
ACTIVE_PANE = f"{MAIN_CSS} .ant-tabs-tabpane-active"


def is_tab_active(d: Driver, tab: int) -> bool:
    try:
        d.waiting(f"#rc-tabs-2-panel-{tab}.ant-tabs-tabpane-active")
        return True
    except NoSuchElementException:
        return False


def change_tab(d: Driver, tab: int):
    d.clicking(f"{NAV_CSS}>div[data-node-key='{tab}']")
    assert is_tab_active(d, tab)
