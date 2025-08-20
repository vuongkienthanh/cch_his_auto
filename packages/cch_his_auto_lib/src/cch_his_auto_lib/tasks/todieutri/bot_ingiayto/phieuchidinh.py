import time
from enum import StrEnum

from selenium.common import StaleElementReferenceException

from cch_his_auto_lib.driver import get_global_driver
from cch_his_auto_lib.tracing import EndOfLoop
from . import _lgr, _trace, goto


class State(StrEnum):
    Sign = "Ký Bác sĩ"
    Cancel = "Hủy ký Bác sĩ"


@_trace
def sign_phieuchidinh():
    "Inside *tờ điều trị*, try to sign *phiếu chỉ định* in sequence"
    _d = get_global_driver()

    def close_dialog():
        _d.clicking(
            ".ant-modal-close:has(~.ant-modal-body .__list)",
            "close dialog button",
        )
        _d.wait_closing(".ant-modal-body .__list", "phieu chi dinh dialog")

    goto(name="Phiếu chỉ định")
    for i in range(120):
        time.sleep(1)
        _lgr.debug(f"checking button state {i}...")
        for ele in _d.find_all(".__button button"):
            try:
                if ele.text == State.Cancel:
                    _lgr.debug(f"button state is {State.Cancel}")
                    close_dialog()
                    return
                elif ele.text == "Ký Bác sĩ":
                    _lgr.debug(f"button state is {State.Sign} -> click")
                    ele.click()
                    time.sleep(5)
                    close_dialog()
                    return
            except StaleElementReferenceException as e:
                _lgr.warning(f"get {e}")
    else:
        close_dialog()
        raise EndOfLoop("can't sign phieuchidinh while in dialog")
