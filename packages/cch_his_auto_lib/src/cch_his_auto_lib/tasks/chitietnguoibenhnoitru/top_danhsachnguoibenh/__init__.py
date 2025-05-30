import logging

from selenium.webdriver import Keys

from cch_his_auto_lib.driver import get_global_driver
from cch_his_auto_lib.helper import tracing
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru import wait_patient_page_loaded
from .. import TOP_BTN_CSS


_lgr = logging.getLogger("top_danhsachnguoibenh")
_trace = tracing(_lgr)

DRAWER_CSS = ".ant-drawer-body"


@_trace
def open_dialog():
    _d = get_global_driver()
    _d.clicking(
        f"{TOP_BTN_CSS}>div:last-child",
        "click Danh sách người bệnh button",
    )
    _d.waiting(DRAWER_CSS, "Danh sách người bệnh panel")


@_trace
def close_dialog():
    _d = get_global_driver()
    _d.clicking(".ant-drawer-mask", "outside Danh sách người bệnh panel")
    _d.wait_closing(DRAWER_CSS, "Danh sách người bệnh panel")


def filter_patient(ma_hs: int):
    "After `open_dialog`, filter patient based on `ma_hs`"
    _d = get_global_driver()
    _lgr.debug(f"ma_hs={ma_hs}")
    ele = _d.clear_input(f"{DRAWER_CSS} .searching input")
    _lgr.debug("+++++ typing ma_hs to search entry")
    ele.send_keys(str(ma_hs))
    ele.send_keys(Keys.ENTER)
    _d.waiting_to_startswith(
        f"{DRAWER_CSS} tbody tr:nth-child(2) td:nth-child(3)", str(ma_hs), "patient id"
    )


@_trace
def goto_patient(ma_hs: int):
    "After `open_dialog`, filter patient based on `ma_hs`, then open that patient"
    _d = get_global_driver()
    _lgr.info(f"goto patient ma_hs={ma_hs}")
    filter_patient(ma_hs)
    _d.clicking(f"{DRAWER_CSS} tbody tr:nth-child(2)", "first row")
    wait_patient_page_loaded(ma_hs)
