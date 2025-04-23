from contextlib import contextmanager

from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import Driver

DIALOG_CSS = ".ant-modal:has(.img-avatar)"
ACTIVE_PANE = f"{DIALOG_CSS} .ant-tabs-tabpane-active"


def open_dialog(driver: Driver):
    driver.clicking(
        ".thong-tin-benh-nhan .bunch-icon div:nth-child(3)", "xem ho so benh an"
    )
    driver.waiting(
        f"{DIALOG_CSS} .right-content tbody tr:nth-child(2)",
        "Danh sách phiếu first item",
    )


def change_tab(driver: Driver, tab: int):
    driver.clicking(f"{DIALOG_CSS} .ant-tabs-nav-list>div:nth-child({tab})")


def close_dialog(driver: Driver):
    driver.clicking(f"{DIALOG_CSS} .ant-modal-close", "close button")
    driver.wait_closing(DIALOG_CSS, "Hồ sơ bệnh án dialog")


def is_active(driver: Driver, tab: int) -> bool:
    try:
        driver.waiting(
            f"{DIALOG_CSS} .ant-tabs-nav-list>div:nth-child({tab})[class='ant-tabs-tab ant-tabs-tab-active']"
        )
        return True
    except NoSuchElementException:
        return False


@contextmanager
def session(driver: Driver, tab: int = 1):
    "use as contextmanager for open and close hosobenhan dialog"
    assert tab > 0
    try:
        open_dialog(driver)
        if tab != 1:
            change_tab(driver, tab)
        assert is_active(driver, tab)
        yield
    finally:
        close_dialog(driver)
