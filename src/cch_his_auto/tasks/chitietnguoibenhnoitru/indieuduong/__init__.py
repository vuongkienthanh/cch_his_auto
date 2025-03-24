"""
### Tasks that operate on *In điều dưỡng*
###### inside "*Chi tiết người bệnh nội trú*
"""

import time
import logging

from selenium.webdriver import Keys

from cch_his_auto.driver import Driver

_logger = logging.getLogger()

def open(driver: Driver):
    driver.clicking(".footer-btn .right button:nth-child(3)", "open In điều dưỡng")
    driver.waiting(".ant-popover .ant-select", "Tìm kiếm tên phiếu in")
    driver.waiting(".ant-popover .ant-select-item", "Tìm kiếm tên phiếu in - item")
    time.sleep(2)

def close(driver: Driver):
    driver.clicking(".footer-btn .right button:nth-child(3)", "close In điều dưỡng")
    time.sleep(2)

def goto(driver: Driver, name: str):
    "After `open`, filter selection based on `name`"
    ele = driver.clear_input(".ant-popover .ant-select input")
    time.sleep(2)
    _logger.info(f"typing {name}")
    ele.send_keys(name)
    time.sleep(2)
    ele.send_keys(Keys.ENTER)
