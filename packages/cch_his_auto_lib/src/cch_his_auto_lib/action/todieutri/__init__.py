import logging

from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tracing import tracing
from cch_his_auto_lib.action.chitietnguoibenhnoitru import (
    wait_patient_page_loaded,
    get_patient_info,
)

URL = "http://emr.ndtp.org/quan-ly-noi-tru/chi-tiet-nguoi-benh-noi-tru/to-dieu-tri"

_lgr = logging.getLogger("todieutri")
_trace = tracing(_lgr)


def get_dienbien(d: Driver) -> str | None:
    try:
        ele = d.waiting("textarea.dien-bien").text.strip()
        if ele == "":
            return None
        else:
            _lgr.info(f"dien bien= {ele}")
            return ele
    except NoSuchElementException:
        _lgr.warning("-> can't find dien bien")
        return None


def back_to_chitietthongtin(d: Driver):
    ma_hs = get_patient_info(d)["ma_hs"]
    d.clicking(".footer-btn .right button:nth-child(2)", "go back button")
    wait_patient_page_loaded(d, int(ma_hs))
