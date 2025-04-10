"""
### Tasks that operate on *Danh sách người bệnh nội trú*
"""

import logging
import time
import datetime as dt

from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

from cch_his_auto.driver import Driver

_logger = logging.getLogger()

URL = "http://emr.ndtp.org/quan-ly-noi-tru/danh-sach-nguoi-benh-noi-tru"
"All tasks in this submodule work under this url."

FMT = "%Y-%m-%d"
"@private"

def filter_trangthainguoibenh(driver: Driver, indexes: list[int]):
    """
    Open *Trạng thái người bệnh*.
    Uncheck all checkboxes, then check those in `indexes`.
    `indexes` is 1-indexed.
    Then close it
    """
    driver.clicking(
        ".base-search_component .ant-col:nth-child(7) button", "trang thai nguoi benh"
    )
    driver.waiting(".ant-popover label", "danh sach trang thai nguoi benh")
    _logger.info("uncheck all boxes in trạng thái người bệnh")
    for ele in driver.find_all(".ant-popover .ant-checkbox-checked"):
        ele.click()

    for i in indexes:
        driver.clicking(
            f".ant-popover label:nth-child({i}) .ant-checkbox",
            driver.find(f".ant-popover label:nth-child({i})").text,
        )
    driver.clicking(
        ".base-search_component .ant-col:nth-child(7) button",
        "trang thai nguoi benh lan 2",
    )

def open_filter_boloc(driver: Driver):
    "Open filter *Bộ lọc* for subsequent tasks"
    _logger.info("opening bo loc")
    driver.clicking(".base-search_component .ant-col:nth-child(1) button", "Bộ lọc")
    driver.waiting(".ant-popover .content-popover +div button", "Tìm button")

def close_filter_boloc(driver: Driver):
    "Close filter *Bộ lọc* after `open_filter_boloc` and finish all tasks inside"
    _logger.info("closing bo loc")
    driver.clicking(".ant-popover .content-popover +div button", "Tìm button")

def filter_boloc_thoigiannhapvien(driver: Driver, start: dt.date, end: dt.date):
    "After `open_filter_boloc`, input admission `start` date and `end` date info"
    start_d = start.strftime(FMT)
    end_d = end.strftime(FMT)
    _logger.info(f"+++++ typing thoi gian vao khoa: {start_d} -> {end_d}")
    ActionChains(driver).send_keys_to_element(
        driver.find(".date-1 .ant-picker-input input"), start_d
    ).pause(1).send_keys_to_element(
        driver.find(".date-1 .ant-picker-input:nth-child(3) input"), end_d
    ).send_keys(Keys.ENTER).perform()

def filter_patient(driver: Driver, ma_hs: int) -> bool:
    "Filter patient based on `ma_hs`"
    ele = driver.clear_input(".base-search_component .ant-col:nth-child(2) input")
    _logger.info(f"+++++ typing {ma_hs} to search entry")
    ele.send_keys(str(ma_hs))
    ele.send_keys(Keys.ENTER)
    time.sleep(2)
    try:
        driver.waiting_to_be(
            ".ant-table-body tbody tr:nth-child(2) td:nth-child(8)",
            str(ma_hs),
            "patient id",
        )
        return True
    except:
        return False

def goto_patient(driver: Driver, ma_hs: int):
    "Filter patient based on `ma_hs`, then open that patient"
    if filter_patient(driver, ma_hs):
        driver.clicking(
            ".ant-table-body tbody tr:nth-child(2) td:nth-child(30)",
            "first row",
        )
        driver.waiting_to_be(
            ".patient-information .ant-row span:nth-child(2) b",
            str(ma_hs),
            "patient id",
        )
