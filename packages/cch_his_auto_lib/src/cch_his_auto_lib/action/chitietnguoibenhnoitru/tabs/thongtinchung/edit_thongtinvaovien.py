from contextlib import contextmanager

from selenium.webdriver import Keys

from cch_his_auto_lib.driver import Driver
from . import THONGTINVAOVIEN_CSS, _lgr


DIALOG_CSS = ".ant-modal:has(.ant-col:nth-child(7) textarea)"


@contextmanager
def session(d: Driver):
    d.clicking2(f"{THONGTINVAOVIEN_CSS} .title svg", "edit thongtinvaovien button")
    d.waiting(DIALOG_CSS, "edit thongtinvaovien dialog")
    try:
        yield
    finally:
        d.clicking(
            f"{DIALOG_CSS} .bottom-action-right button",
            "save button",
        )
        d.wait_closing(DIALOG_CSS, "edit thongtinravien dialog")


def set_bloodtype(d: Driver, value: str):
    _lgr.info(f"set bloodtype= {value}")
    ele = d.clear_input(f"{DIALOG_CSS} .ant-col:nth-child(4) input")
    ele.send_keys(value)
    ele.send_keys(Keys.ENTER)
