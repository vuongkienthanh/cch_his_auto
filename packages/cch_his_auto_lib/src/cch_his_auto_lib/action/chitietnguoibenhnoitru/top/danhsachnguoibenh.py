import logging
from contextlib import contextmanager

from selenium.webdriver import Keys

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tracing import tracing
from cch_his_auto_lib.action.chitietnguoibenhnoitru import (
    wait_loaded,
    get_patient_info,
)
from . import TOP_BTN_CSS


_lgr = logging.getLogger("top_danhsachnguoibenh")
_trace = tracing(_lgr)

DRAWER_CSS = ".ant-drawer-body"


@contextmanager
def session(d: Driver):
    if get_patient_info(d)["doituong"] == "Bảo hiểm":
        d.clicking(f"{TOP_BTN_CSS}>div:nth-last-child(3)")
    else:
        d.clicking(f"{TOP_BTN_CSS}>div:nth-last-child(2)")
    d.waiting(DRAWER_CSS)
    try:
        yield
    finally:
        # d.clicking(".ant-drawer-mask", "outside Danh sách người bệnh panel")
        # d.wait_closing(DRAWER_CSS, "Danh sách người bệnh panel")
        pass


@_trace
def goto_patient(d: Driver, ma_hs: int):
    "After `open_dialog`, filter patient based on `ma_hs`, then open that patient"
    _lgr.info(f"goto patient ma_hs={ma_hs}")
    with session(d):
        ele = d.clear_input(f"{DRAWER_CSS} .searching input")
        ele.send_keys(str(ma_hs))
        ele.send_keys(Keys.ENTER)
        d.wait_disappearing(f"{DRAWER_CSS} tbody tr:nth-child(3)")
        d.clicking(f"{DRAWER_CSS} tbody tr:nth-child(2)", "first row")
        wait_loaded(d)
