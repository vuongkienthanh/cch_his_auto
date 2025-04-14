import time
import logging

from selenium.common import StaleElementReferenceException

from cch_his_auto.driver import Driver
from . import open_menu, goto

_logger = logging.getLogger().getChild("tasks")

def sign_phieuchidinh(driver: Driver):
    "Inside *tờ điều trị*, try to sign *phiếu chỉ định* in sequence"

    def _close_dialog():
        driver.clicking(
            ".ant-modal-close:has(~.ant-modal-body .__list)",
            "close dialog button",
        )
        _logger.info("finish signing phieuchidinh")

    open_menu(driver)
    goto(driver, name="Phiếu chỉ định")
    for _ in range(120):
        time.sleep(1)
        _logger.debug("checking Hủy ký bác sĩ")
        for w in driver.find_all(".__button button"):
            try:
                if w.text == "Hủy ký Bác sĩ":
                    _logger.debug("found Hủy ký bác sĩ")
                    _close_dialog()
                    return
                elif w.text == "Ký Bác sĩ":
                    _logger.debug("found Ký bác sĩ -> click sign button")
                    w.click()
                    time.sleep(5)
                    _close_dialog()
                    return
            except StaleElementReferenceException:
                _logger.warning("get StaleElementReferenceException")
    else:
        _logger.error("can't sign phieuchidinh while in dialog")
        raise Exception("can't sign phieuchidinh while in dialog")
