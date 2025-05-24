from contextlib import contextmanager

from selenium.webdriver import Keys

from cch_his_auto_lib.driver import get_global_driver
from . import THONGTINVAOVIEN_CSS, _lgr


DIALOG_CSS = ".ant-modal:has(.ant-col:nth-child(6) textarea)"


@contextmanager
def session():
    open_dialog()
    try:
        yield
    finally:
        save()


def open_dialog():
    _d = get_global_driver()
    _d.clicking2(f"{THONGTINVAOVIEN_CSS} .title svg", "edit thongtinvaovien button")
    _d.waiting(DIALOG_CSS, "edit thongtinvaovien dialog")


def save():
    _d = get_global_driver()
    _d.clicking(
        f"{DIALOG_CSS} .bottom-action-right button",
        "save button",
    )
    _d.wait_closing(DIALOG_CSS, "edit thongtinravien dialog")


def set_bloodtype(value: str):
    _d = get_global_driver()
    _lgr.info(f"set bloodtype= {value}")
    ele = _d.clear_input(f"{DIALOG_CSS} .ant-col:nth-child(4) input")
    ele.send_keys(value)
    ele.send_keys(Keys.ENTER)
