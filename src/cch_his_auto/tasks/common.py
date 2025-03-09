"""
### Tasks that can happen at any place
"""

import logging
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import NoSuchElementException

from cch_his_auto.driver import Driver

_logger = logging.getLogger()

def choose_dept(driver: Driver, dept: str):
    "Choose department with exact `dept`"
    for _ in range(120):
        time.sleep(1)
        try:
            ele = driver.find(".ant-modal-body input")
            _logger.info("found dept picker")
            ActionChains(driver).send_keys_to_element(
                ele, Keys.ARROW_DOWN
            ).send_keys_to_element(ele, dept).send_keys_to_element(
                ele, Keys.ENTER
            ).click(
                driver.find(
                    ".ant-modal-body .bottom-action .bottom-action-right button"
                )
            ).perform()
            break
        except:
            try:
                ele = driver.find(".khoaLamViec div span")
                if ele.text.strip() == dept:
                    _logger.info("dept already set")
                    break
                else:
                    _logger.info(f"dept not set to {dept}")
                    driver.clicking(".khoaLamViec div span")
            except NoSuchElementException:
                ...

__all__ = ["choose_dept"]
