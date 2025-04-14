import time
import logging

from cch_his_auto.driver import Driver
from . import open_menu, goto

_logger = logging.getLogger()

def sign_phieuchidinh(driver: Driver):
    "Inside *tờ điều trị*, try to sign *phiếu chỉ định* in sequence"
    open_menu(driver)
    goto(driver, name="Phiếu chỉ định")
    finish = False
    for _ in range(20):
        time.sleep(1)
        _logger.info("checking Hủy ký bác sĩ")
        for w in driver.find_all(".__button button"):
            if w.text == "Hủy ký Bác sĩ":
                finish = True
                break
        if finish:
            logging.info("phieu chi dinh already signed")
            break
        for w in driver.find_all(".__button button"):
            if w.text == "Ký Bác sĩ":
                _logger.info("clicking Ký bác sĩ")
                w.click()
                time.sleep(5)
                break
    else:
        raise Exception("cant sign phieuchidinh while in dialog")
    driver.clicking(
        ".ant-modal-close:has(~.ant-modal-body .__list)", "close dialog button"
    )
