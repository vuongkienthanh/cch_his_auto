import time
import logging

from selenium.webdriver import Keys

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.helper import tracing

_logger = logging.getLogger("bot_indieuduong")
_trace = tracing(_logger)


def goto(driver: Driver, name: str):
    "Open menu *In điều dưỡng*, filter selection based on `name`"
    driver.clicking(".footer-btn .right button:nth-child(3)", "open In điều dưỡng")
    driver.waiting(".ant-popover .ant-select", "Tìm kiếm tên phiếu in")
    driver.waiting(".ant-popover .ant-select-item", "Tìm kiếm tên phiếu in - item")
    _logger.info(f"goto name={name}")
    ele = driver.clear_input(".ant-popover .ant-select input")
    ele.send_keys(name)
    time.sleep(2)
    ele.send_keys(Keys.ENTER)


from .bangkechiphiBHYT import sign_bangkechiphiBHYT
from .camketchungvenhapvien import get_signature

__all__ = ["sign_bangkechiphiBHYT", "get_signature"]
