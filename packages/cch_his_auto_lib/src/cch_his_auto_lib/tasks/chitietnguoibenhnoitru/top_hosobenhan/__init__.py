from contextlib import contextmanager
import logging

from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru import TOP_BTN_CSS

_lgr = logging.getLogger("top_hosobenhan")

DIALOG_CSS = ".ant-modal:has(.img-avatar)"
NAV_CSS = f"{DIALOG_CSS} .ant-tabs-nav-list"
ACTIVE_PANE = f"{DIALOG_CSS} .ant-tabs-tabpane-active"


@contextmanager
def session(d: Driver, tab: int = 1):
    "use as contextmanager for open and close hosobenhan dialog"
    assert tab > 0
    try:
        open_dialog(d)
        if tab != 1:
            change_tab(d, tab)
        yield
    finally:
        close_dialog(d)


def open_dialog(d: Driver):
    d.clicking(f"{TOP_BTN_CSS}>div:nth-child(3)", "xem ho so benh an")
    d.waiting(
        f"{DIALOG_CSS} .right-content tbody tr:nth-child(2)",
        "Danh sách phiếu first item",
    )


def change_tab(d: Driver, tab: int):
    d.clicking(f"{NAV_CSS}>div:nth-child({tab})")
    assert is_tab_active(d, tab)


def close_dialog(d: Driver):
    d.clicking(f"{DIALOG_CSS} .ant-modal-close", "close button")
    d.wait_closing(DIALOG_CSS, "Hồ sơ bệnh án dialog")


def is_tab_active(d:Driver, tab: int) -> bool:
    try:
        d.waiting(
            f"{NAV_CSS}>div:nth-child({tab})[class='ant-tabs-tab ant-tabs-tab-active']"
        )
        return True
    except NoSuchElementException:
        return False
