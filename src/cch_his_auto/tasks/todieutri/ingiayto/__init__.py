import logging
import time

from cch_his_auto.driver import Driver
from cch_his_auto.helper import tracing, EndOfLoop

_logger = logging.getLogger().getChild("tasks.ingiayto")
_trace = tracing(_logger)

@_trace
def open_menu(driver: Driver):
    "Open menu *In giấy tờ*"
    driver.clicking(".footer-btn .right button:nth-child(1)", "open menu In giấy tờ")

@_trace
def goto(driver: Driver, name: str):
    "After `open_menu`, click `name`"
    for i in range(120):
        time.sleep(1)
        _logger.debug(f"finding link {name} {i}...")
        for ele in driver.find_all(".ant-dropdown li div div , .ant-dropdown li a"):
            if ele.text == name:
                _logger.debug(f"-> found link {name} -> proceed to click link")
                ele.click()
                _logger.debug("-> finish click link")
                time.sleep(2)
                return
    else:
        driver.clicking(
            ".footer-btn .right button:nth-child(1)", "close menu In giấy tờ"
        )
        raise EndOfLoop(f"can't goto {name}")

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
