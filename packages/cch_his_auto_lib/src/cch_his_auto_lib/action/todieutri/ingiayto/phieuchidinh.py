import time
from enum import StrEnum

from selenium.common import StaleElementReferenceException

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.errors import EndOfLoopException

from . import _lgr, _trace, goto


DIALOG = ".ant-modal:has(.__list)"


class State(StrEnum):
    Trinh = "Trình ký"
    Ky = "Ký Bác sĩ"
    Huy = "Hủy ký Bác sĩ"


@_trace
def sign_phieuchidinh(d: Driver):
    "Inside *tờ điều trị*, try to sign *phiếu chỉ định* in sequence"

    goto(d, name="Phiếu chỉ định")
    d.waiting_to_startswith(f"{DIALOG} .__button > button:nth-child(2)", State.Trinh)
    d.waiting_to_startswith(f"{DIALOG} .__button > button:first-child", State.Ky)
    d.clicking(f"{DIALOG} .__button > button:first-child")
    try:
        for i in range(120):
            time.sleep(1)
            _lgr.debug(f"checking button state {i}...")
            for ele in d.find_all(f"{DIALOG} .__button > button"):
                try:
                    if ele.text == State.Huy:
                        _lgr.debug(f"button state is {State.Huy}")
                        break
                except StaleElementReferenceException as e:
                    _lgr.warning(f"get {e}")
        else:
            raise EndOfLoopException("can't assure phieuchidinh signed while in dialog")
    finally:
        d.clicking(f"{DIALOG} button.ant-modal-close")
        d.wait_disappearing(DIALOG)
