import time
from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.helper import tracing, EndOfLoop
from .. import _logger

_logger = _logger.getChild("ingiayto")
_trace = tracing(_logger)


def goto(driver: Driver, name: str):
    "Open menu *In giấy tờ*, click `name`"
    driver.clicking(".footer-btn .right button:nth-child(1)", "open menu In giấy tờ")
    _logger.info(f"goto name={name}")
    for i in range(120):
        time.sleep(1)
        _logger.debug(f"finding link {name} {i}...")
        for ele in driver.find_all(".ant-dropdown li div div , .ant-dropdown li a"):
            if ele.text == name:
                _logger.debug(f"-> found link {name} -> proceed to click link")
                ele.click()
                time.sleep(2)
                return
    else:
        driver.clicking(
            ".footer-btn .right button:nth-child(1)", "close menu In giấy tờ"
        )
        raise EndOfLoop(f"can't goto {name}")


from .todieutri import sign_todieutri
from .phieuchidinh import sign_phieuchidinh
from .phieuthuchienylenh import (
    sign_phieuthuchienylenh_bs,
    sign_phieuthuchienylenh_dd,
    sign_phieuthuchienylenh_bn,
)

__all__ = [
    "goto",
    "sign_todieutri",
    "sign_phieuchidinh",
    "sign_phieuthuchienylenh_bs",
    "sign_phieuthuchienylenh_dd",
    "sign_phieuthuchienylenh_bn",
]
