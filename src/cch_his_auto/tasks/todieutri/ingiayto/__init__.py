"""
### Tasks: In giấy tờ
Mostly about clicking Sign buttons
"""

import logging
import time

from cch_his_auto.driver import Driver

_logger = logging.getLogger()

def open_menu(driver: Driver):
    "Click *In giấy tờ* button"
    driver.clicking(".footer-btn .right button:nth-child(1)", "open In giấy tờ")

def goto(driver: Driver, name: str):
    "After `open_menu`, click `name`"
    _logger.info(f"======= finding link {name} ======")
    for _ in range(30):
        time.sleep(1)
        for ele in driver.find_all(".ant-dropdown li div div , .ant-dropdown li a"):
            if ele.text == name:
                ele.click()
                _logger.info(f"======= found link {name} ======")
                time.sleep(2)
                return
    else:
        _logger.warning(f"cant find {name}")
        driver.clicking(".footer-btn .right button:nth-child(1)")
        raise Exception(f"cant find {name}")

from .phieuchidinh import sign_phieuchidinh
from .todieutri import sign_todieutri
from .phieuthuchienylenh import (
    sign_phieuthuchienylenh_bn,
    sign_phieuthuchienylenh_bs,
    sign_phieuthuchienylenh_dd,
)

__all__ = [
    "open_menu",
    "goto",
    "sign_phieuchidinh",
    "sign_todieutri",
    "sign_phieuthuchienylenh_bs",
    "sign_phieuthuchienylenh_dd",
    "sign_phieuthuchienylenh_bn",
]
