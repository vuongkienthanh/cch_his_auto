from contextlib import contextmanager
import logging

from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import get_global_driver
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru import TOP_BTN_CSS

_lgr = logging.getLogger("top_hosobenhan")

DIALOG_CSS = ".ant-modal:has(.img-avatar)"
NAV_CSS = f"{DIALOG_CSS} .ant-tabs-nav-list"
ACTIVE_PANE = f"{DIALOG_CSS} .ant-tabs-tabpane-active"


@contextmanager
def session(tab: int = 1):
    "use as contextmanager for open and close hosobenhan dialog"
    assert tab > 0
    try:
        open_dialog()
        if tab != 1:
            change_tab(tab)
        yield
    finally:
        close_dialog()


def open_dialog():
    _d = get_global_driver()
    _d.clicking(f"{TOP_BTN_CSS}>div:nth-child(3)", "xem ho so benh an")
    _d.waiting(
        f"{DIALOG_CSS} .right-content tbody tr:nth-child(2)",
        "Danh sách phiếu first item",
    )


def change_tab(tab: int):
    _d = get_global_driver()
    _d.clicking(f"{NAV_CSS}>div:nth-child({tab})")
    assert is_tab_active(tab)


def close_dialog():
    _d = get_global_driver()
    _d.clicking(f"{DIALOG_CSS} .ant-modal-close", "close button")
    _d.wait_closing(DIALOG_CSS, "Hồ sơ bệnh án dialog")


def is_tab_active(tab: int) -> bool:
    _d = get_global_driver()
    try:
        _d.waiting(
            f"{NAV_CSS}>div:nth-child({tab})[class='ant-tabs-tab ant-tabs-tab-active']"
        )
        return True
    except NoSuchElementException:
        return False
