import time
import logging

from selenium.webdriver import Keys

from cch_his_auto.driver import Driver
from cch_his_auto.helper import tracing

_logger = logging.getLogger().getChild("indieuduong")
_trace = tracing(_logger)


def open_menu(driver: Driver):
    "Open menu *In điều dưỡng* from *Chi tiết người bệnh nội trú*"
    driver.clicking(".footer-btn .right button:nth-child(3)", "open In điều dưỡng")
    driver.waiting(".ant-popover .ant-select", "Tìm kiếm tên phiếu in")
    driver.waiting(".ant-popover .ant-select-item", "Tìm kiếm tên phiếu in - item")


@_trace
def goto(driver: Driver, name: str):
    "After `open_menu`, filter selection based on `name`"
    _logger.info(f"goto name={name}")
    ele = driver.clear_input(".ant-popover .ant-select input")
    ele.send_keys(name)
    time.sleep(2)
    ele.send_keys(Keys.ENTER)
