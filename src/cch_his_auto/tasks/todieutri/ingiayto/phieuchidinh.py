import time
import logging
from enum import StrEnum

from selenium.common import StaleElementReferenceException

from cch_his_auto.driver import Driver
from cch_his_auto.helper import tracing, EndOfLoop
from .helper import open_menu, goto

_logger = logging.getLogger().getChild("ingiayto")
_trace = tracing(_logger)


class _State(StrEnum):
    Sign = "Ký Bác sĩ"
    Cancel = "Hủy ký Bác sĩ"


@_trace
def sign_phieuchidinh(driver: Driver):
    "Inside *tờ điều trị*, try to sign *phiếu chỉ định* in sequence"

    def _close_dialog():
        driver.clicking(
            ".ant-modal-close:has(~.ant-modal-body .__list)",
            "close dialog button",
        )

    open_menu(driver)
    goto(driver, name="Phiếu chỉ định")
    for i in range(120):
        time.sleep(1)
        _logger.debug(f"checking button state {i}...")
        for ele in driver.find_all(".__button button"):
            try:
                if ele.text == _State.Cancel:
                    _logger.debug(f"button state is {_State.Cancel}")
                    _close_dialog()
                    return
                elif ele.text == "Ký Bác sĩ":
                    _logger.debug(f"button state is {_State.Sign} -> click")
                    ele.click()
                    time.sleep(5)
                    _close_dialog()
                    return
            except StaleElementReferenceException as e:
                _logger.warning(f"get {e}")
    else:
        _close_dialog()
        raise EndOfLoop("can't sign phieuchidinh while in dialog")
