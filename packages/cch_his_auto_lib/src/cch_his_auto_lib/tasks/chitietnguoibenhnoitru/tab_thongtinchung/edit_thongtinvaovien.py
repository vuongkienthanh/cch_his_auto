from contextlib import contextmanager

from selenium.webdriver import Keys

from cch_his_auto_lib.driver import Driver
from . import THONGTINVAOVIEN_CSS

DIALOG_CSS = ".ant-modal:has(.ant-col:nth-child(6) textarea)"


@contextmanager
def session(driver: Driver):
    open_dialog(driver)
    try:
        yield
    finally:
        save(driver)


def open_dialog(driver: Driver):
    driver.clicking_svg(
        f"{THONGTINVAOVIEN_CSS} .title svg", "edit thongtinvaovien button"
    )
    driver.waiting(DIALOG_CSS, "edit thongtinvaovien dialog")


def save(driver: Driver):
    driver.clicking(
        f"{DIALOG_CSS} .bottom-action-right button",
        "save button",
    )
    driver.wait_closing(DIALOG_CSS, "edit thongtinra vien dialog")


def set_bloodtype(driver: Driver, value: str):
    ele = driver.clear_input(f"{DIALOG_CSS} .ant-col:nth-child(4) input")
    ele.send_keys(value)
    ele.send_keys(Keys.ENTER)
