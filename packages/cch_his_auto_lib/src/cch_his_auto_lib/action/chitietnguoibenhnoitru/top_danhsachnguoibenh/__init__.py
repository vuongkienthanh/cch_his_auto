import logging

from selenium.webdriver import Keys

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tracing import tracing
from cch_his_auto_lib.action.chitietnguoibenhnoitru import wait_patient_page_loaded
from .. import TOP_BTN_CSS


_lgr = logging.getLogger("top_danhsachnguoibenh")
_trace = tracing(_lgr)

DRAWER_CSS = ".ant-drawer-body"


@_trace
def open_dialog(d: Driver):
    d.clicking(
        f"{TOP_BTN_CSS}>div:last-child",
        "click Danh sách người bệnh button",
    )
    d.waiting(DRAWER_CSS, "Danh sách người bệnh panel")


@_trace
def close_dialog(d: Driver):
    d.clicking(".ant-drawer-mask", "outside Danh sách người bệnh panel")
    d.wait_closing(DRAWER_CSS, "Danh sách người bệnh panel")


def filter_patient(d: Driver, ma_hs: int):
    "After `open_dialog`, filter patient based on `ma_hs`"
    _lgr.debug(f"ma_hs={ma_hs}")
    ele = d.clear_input(f"{DRAWER_CSS} .searching input")
    _lgr.debug("+++++ typing ma_hs to search entry")
    ele.send_keys(str(ma_hs))
    ele.send_keys(Keys.ENTER)
    d.waiting_to_startswith(
        f"{DRAWER_CSS} tbody tr:nth-child(2) td:nth-child(3)", str(ma_hs), "patient id"
    )


@_trace
def goto_patient(d: Driver, ma_hs: int):
    "After `open_dialog`, filter patient based on `ma_hs`, then open that patient"
    _lgr.info(f"goto patient ma_hs={ma_hs}")
    filter_patient(d, ma_hs)
    d.clicking(f"{DRAWER_CSS} tbody tr:nth-child(2)", "first row")
    wait_patient_page_loaded(d, ma_hs)
