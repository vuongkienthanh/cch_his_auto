import logging
import time

from selenium.webdriver import Keys

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.helper import tracing

_logger = logging.getLogger().getChild("danhsachnguoibenh")
_trace = tracing(_logger)


@_trace
def open_dialog(driver: Driver):
    driver.clicking(
        ".thong-tin-benh-nhan .bunch-icon div:last-child",
        "click Danh sách người bệnh button",
    )
    driver.waiting(".ant-drawer .searching input", "Danh sách người bệnh panel")


@_trace
def close_dialog(driver: Driver):
    driver.clicking(".ant-drawer-mask", "outside Danh sách người bệnh panel")
    driver.wait_closing(".ant-drawer .searching input", "Danh sách người bệnh panel")


def filter_patient(driver: Driver, ma_hs: int):
    "After `open_dialog`, filter patient based on `ma_hs`"
    _logger.debug(f"ma_hs={ma_hs}")
    ele = driver.clear_input(".ant-drawer .searching input")
    _logger.debug("+++++ typing ma_hs to search entry")
    ele.send_keys(str(ma_hs))
    ele.send_keys(Keys.ENTER)
    time.sleep(2)
    driver.waiting_to_be(
        "tbody tr:nth-child(2) td:nth-child(3)", str(ma_hs), "patient id"
    )


@_trace
def goto_patient(driver: Driver, ma_hs: int):
    "After `open_dialog`, filter patient based on `ma_hs`, then open that patient"
    _logger.info(f"goto patient ma_hs={ma_hs}")
    filter_patient(driver, ma_hs)
    driver.clicking("tbody tr:nth-child(2)", "first row")
    driver.waiting_to_be(
        ".patient-information .ant-row span:nth-child(2) b",
        str(ma_hs),
        "patient id",
    )
