import logging
import time
import datetime as dt

from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

from cch_his_auto.driver import Driver
from cch_his_auto.helper import tracing

_logger = logging.getLogger().getChild("danhsachnguoibenhnoitru")
_trace = tracing(_logger)

URL = "http://emr.ndtp.org/quan-ly-noi-tru/danh-sach-nguoi-benh-noi-tru"

_FMT = "%Y-%m-%d"


@_trace
def filter_trangthainguoibenh(driver: Driver, indexes: list[int]):
    """
    Open *Trạng thái người bệnh*.
    Uncheck all checkboxes, then check those in `indexes`.
    `indexes` is 1-indexed.
    Then close it
    """
    _logger.debug(f"filter_trangthainguoibenh indexes={indexes}")
    driver.clicking(
        ".base-search_component .ant-col:nth-child(7) button",
        " open menu trạng thái người bệnh",
    )
    driver.waiting(".ant-popover label", "danh sách trạng thái người bệnh")
    _logger.debug("uncheck all boxes in trạng thái người bệnh")
    for ele in driver.find_all(".ant-checkbox-group .ant-checkbox-checked"):
        ele.click()

    _logger.debug("check boxes based on indexes")
    for i in indexes:
        driver.clicking(
            f".ant-checkbox-group label:nth-child({i}) .ant-checkbox",
            driver.find(f".ant-popover label:nth-child({i})").text,
        )
    driver.clicking(
        ".base-search_component .ant-col:nth-child(7) button",
        "close menu trạng thái người bệnh",
    )


@_trace
def open_filter_boloc(driver: Driver):
    "Open filter *Bộ lọc* for subsequent tasks"
    driver.clicking(
        ".base-search_component .ant-col:nth-child(1) button", "Bộ lọc button"
    )
    driver.waiting(".ant-popover .content-popover +div button", "Tìm button")


@_trace
def close_filter_boloc(driver: Driver):
    "Close filter *Bộ lọc* after `open_filter_boloc` and finish all tasks inside"
    driver.clicking(".ant-popover .content-popover +div button", "Tìm button")


@_trace
def filter_boloc_thoigiannhapvien(driver: Driver, start: dt.date, end: dt.date):
    "After `open_filter_boloc`, input admission `start` date and `end` date info"
    _logger.debug(f"start_date={start}")
    _logger.debug(f"end_date={end}")
    start_d = start.strftime(_FMT)
    end_d = end.strftime(_FMT)
    _logger.debug("+++++ typing dates")
    ActionChains(driver).send_keys_to_element(
        driver.find(".date-1 .ant-picker-input input"), start_d
    ).pause(1).send_keys_to_element(
        driver.find(".date-1 .ant-picker-input:nth-child(3) input"), end_d
    ).send_keys(Keys.ENTER).perform()


@_trace
def filter_patient(driver: Driver, ma_hs: int):
    "Filter patient based on `ma_hs`"
    _logger.debug(f"filter_patient ma_hs={ma_hs}")
    ele = driver.clear_input(".base-search_component .ant-col:nth-child(2) input")
    _logger.debug("+++++ typing ma_hs to search entry")
    ele.send_keys(str(ma_hs))
    ele.send_keys(Keys.ENTER)
    time.sleep(2)
    driver.waiting_to_be(
        ".ant-table-body tbody tr:nth-child(2) td:nth-child(8)",
        str(ma_hs),
        "first row patient id",
    )


@_trace
def goto_patient(driver: Driver, ma_hs: int):
    "Filter patient based on `ma_hs`, then open that patient"
    _logger.info(f"goto patient ma_hs={ma_hs}")
    filter_patient(driver, ma_hs)
    driver.clicking(
        ".ant-table-body tbody tr:nth-child(2) td:nth-child(30)",
        "first row",
    )
    driver.waiting_to_be(
        ".patient-information .ant-row span:nth-child(2) b",
        str(ma_hs),
        "patient id",
    )
