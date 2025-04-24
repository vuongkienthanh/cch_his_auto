from contextlib import contextmanager
import logging

from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru.upper_patient_info_buttons import (
    ICON_CSS,
)

DIALOG_CSS = ".ant-modal:has(.img-avatar)"
NAV_CSS = f"{DIALOG_CSS} .ant-tabs-nav-list"
ACTIVE_PANE = f"{DIALOG_CSS} .ant-tabs-tabpane-active"

_logger = logging.getLogger().getChild("hosobenhan")


@contextmanager
def session(driver: Driver, tab: int = 1):
    "use as contextmanager for open and close hosobenhan dialog"
    assert tab > 0
    try:
        open_dialog(driver)
        if tab != 1:
            change_tab(driver, tab)
        yield
    finally:
        close_dialog(driver)


def open_dialog(driver: Driver):
    driver.clicking(f"{ICON_CSS}>div:nth-child(3)", "xem ho so benh an")
    driver.waiting(
        f"{DIALOG_CSS} .right-content tbody tr:nth-child(2)",
        "Danh sách phiếu first item",
    )


def change_tab(driver: Driver, tab: int):
    driver.clicking(f"{NAV_CSS}>div:nth-child({tab})")
    assert is_tab_active(driver, tab)


def close_dialog(driver: Driver):
    driver.clicking(f"{DIALOG_CSS} .ant-modal-close", "close button")
    driver.wait_closing(DIALOG_CSS, "Hồ sơ bệnh án dialog")


def is_tab_active(driver: Driver, tab: int) -> bool:
    try:
        driver.waiting(
            f"{NAV_CSS}>div:nth-child({tab})[class='ant-tabs-tab ant-tabs-tab-active']"
        )
        return True
    except NoSuchElementException:
        return False
