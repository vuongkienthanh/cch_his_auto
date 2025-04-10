"""
### Tasks that operate on *In điều dưỡng*
###### inside "*Chi tiết người bệnh nội trú*
"""

import time
import logging

from selenium.webdriver import Keys

from cch_his_auto.driver import Driver

_logger = logging.getLogger()

def open_menu(driver: Driver):
    driver.clicking(".footer-btn .right button:nth-child(3)", "open In điều dưỡng")
    driver.waiting(".ant-popover .ant-select", "Tìm kiếm tên phiếu in")
    driver.waiting(".ant-popover .ant-select-item", "Tìm kiếm tên phiếu in - item")

def goto(driver: Driver, name: str):
    "After `open_menu`, filter selection based on `name`"
    ele = driver.clear_input(".ant-popover .ant-select input")
    _logger.info(f"typing {name}")
    ele.send_keys(name)
    time.sleep(2)
    ele.send_keys(Keys.ENTER)

from .bangkechiphiBHYT import sign_bangkechiphiBHYT

__all__ = [
    "open_menu",
    "goto",
    "sign_bangkechiphiBHYT",
]
