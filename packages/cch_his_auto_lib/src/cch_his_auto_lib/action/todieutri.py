import logging
import time
from enum import StrEnum

from selenium.common import NoSuchElementException, StaleElementReferenceException

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tracing import tracing
from cch_his_auto_lib.errors import EndOfLoopException
from cch_his_auto_lib.action.chitietnguoibenhnoitru import (
    wait_loaded,
    get_patient_info,
)

URL = "http://emr.ndtp.org/quan-ly-noi-tru/chi-tiet-nguoi-benh-noi-tru/to-dieu-tri"

_lgr = logging.getLogger("todieutri")
_trace = tracing(_lgr)


def wait_loaded(d: Driver):
    d.waiting("#root .patient-information")
    p = get_patient_info(d)
    _lgr.info(f"Patient page loaded: {p['name']} ,{p['ma_hs']}")


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
    d.clicking(".footer-btn .right button:nth-child(2)", "go back button")
    wait_loaded(d)


@_trace
def ingiayto(d: Driver, name: str):
    d.clicking(".footer-btn .right button:nth-child(1)", "open menu In giấy tờ")
    _lgr.info(f"ingiayto -> {name}")
    for i in range(120):
        time.sleep(1)
        _lgr.debug(f"finding link {name} {i}...")
        for ele in d.find_all(".ant-dropdown li div div , .ant-dropdown li a"):
            if ele.text == name:
                _lgr.debug(f"-> found link {name} -> proceed to click link")
                ele.click()
                time.sleep(2)
                return
    else:
        d.clicking(".footer-btn .right button:nth-child(1)", "close menu In giấy tờ")
        raise EndOfLoopException(f"can't find ingiayto -> {name}")


def phieuchidinh(d: Driver):
    "Inside *tờ điều trị*, try to sign *phiếu chỉ định*"

    PHIEUCHIDINH_DIALOG = ".ant-modal:has(.__list)"

    class State(StrEnum):
        Trinh = "Trình ký"
        Ky = "Ký Bác sĩ"
        Huy = "Hủy ký Bác sĩ"

    ingiayto(d, "Phiếu chỉ định")
    d.waiting_to_startswith(
        f"{PHIEUCHIDINH_DIALOG} .__button > button:nth-child(2)", State.Trinh
    )
    d.waiting_to_startswith(
        f"{PHIEUCHIDINH_DIALOG} .__button > button:first-child", State.Ky
    )
    d.clicking(f"{PHIEUCHIDINH_DIALOG} .__button > button:first-child")
    try:
        for i in range(30):
            time.sleep(1)
            _lgr.debug(f"checking button state {i}...")
            for ele in d.find_all(f"{PHIEUCHIDINH_DIALOG} .__button > button"):
                try:
                    if ele.text == State.Huy:
                        _lgr.debug(f" found button state is {State.Huy}")
                        break
                except StaleElementReferenceException as e:
                    _lgr.warning(f"get {e}")
        else:
            _lgr.warning("can't assure phieuchidinh signed while in dialog, maybe MRI")
    finally:
        d.clicking(f"{PHIEUCHIDINH_DIALOG} button.ant-modal-close")
        d.wait_disappearing(PHIEUCHIDINH_DIALOG)
