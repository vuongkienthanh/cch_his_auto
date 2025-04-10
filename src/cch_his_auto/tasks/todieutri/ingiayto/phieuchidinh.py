import time
import logging

from cch_his_auto.driver import Driver
from . import open_menu, goto

_logger = logging.getLogger()

def sign_phieuchidinh(driver: Driver):
    try:
        open_menu(driver)
        goto(driver, name="Phiếu chỉ định")
    except:
        return
    else:
        finish = False
        for _ in range(45):
            time.sleep(1)
            _logger.info("checking finish the sign button ")
            for w in driver.find_all(".__button button"):
                if w.text == "Hủy ký Bác sĩ":
                    finish = True
                    break
            if finish:
                logging.info("phieu chi dinh already signed")
                break
            for w in driver.find_all(".__button button"):
                if w.text == "Ký Bác sĩ":
                    _logger.info("clicking the sign button ")
                    w.click()
                    time.sleep(5)
                    break
        logging.info("clicking close button")
        driver.find(".ant-modal-close:has(~.ant-modal-body .__list)").click()
        logging.info("finish phieu chi dinh")
        time.sleep(3)
