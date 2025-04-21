import time
import logging
from enum import StrEnum
from typing import Callable

from selenium.webdriver import Keys
from selenium.common import NoSuchElementException, StaleElementReferenceException

from cch_his_auto.driver import Driver, DriverFn

_logger = logging.getLogger().getChild("hosobenhan")


class Status(StrEnum):
    "Possible status for each document"

    CHUAKY = "Chưa ký"
    DANGKY = "Đang ký"
    HOANTHANH = "Hoàn thành"


def open_dialog(driver: Driver):
    driver.clicking(
        ".thong-tin-benh-nhan .bunch-icon div:nth-child(3)", "xem ho so benh an"
    )
    driver.waiting(
        ".ant-modal:has(.img-avatar) .right-content tr:nth-child(2)",
        "Danh sách phiếu first item",
    )


def close_dialog(driver: Driver):
    driver.clicking(".ant-modal:has(.img-avatar) .ant-modal-close", "close button")
    driver.wait_closing(".ant-modal .img-avatar", "Hồ sơ bệnh án dialog")


def filter(driver: Driver, name: str) -> bool:
    "Filter document based on `name`"
    _logger.debug(f"name={name}")
    ele = driver.clear_input(".right-content .header input")
    _logger.debug("+++++ typing name")
    ele.send_keys(name)
    ele.send_keys(Keys.ENTER)
    for _ in range(60):  # 120 is too long
        time.sleep(1)
        try:
            ele = driver.find(
                ".right-content tbody tr:nth-child(2) td:nth-child(2) div"
            )
            if ele.text.strip().startswith(name):
                _logger.info(f"-> found {name}")
                return True
        except NoSuchElementException:
            ...
    else:
        _logger.warning(f"-> filtered {name} with no result")
        return False


def is_row(driver: Driver, idx: int, status: Status) -> bool:
    "Check if row at `idx` is `status`, first row is idx=2"
    try:
        _logger.debug(f"checking status = {status}")
        return (
            driver.waiting(
                f".ant-table-tbody tr:nth-child({idx}) td:nth-child(3)",
                f"row {idx} status",
            ).text.strip()
            == status
        )
    except StaleElementReferenceException:
        return is_row(driver, idx, status)


def is_row_expandable(driver: Driver, idx: int) -> bool:
    "Check if row at `idx` is expandable, first row is idx=2"
    name = driver.waiting(
        f".ant-table-tbody tr:nth-child({idx}) td:nth-child(2)", f"row {idx}"
    ).text
    _logger.debug(f"checking {name}: expandable")
    for _ in range(5):
        time.sleep(1)
        try:
            ele = driver.find(
                f".right-content tbody tr:nth-child({idx}) td:nth-child(1) button"
            )
            class_list = ele.get_attribute("class")
            assert class_list is not None
            return "ant-table-row-expand-icon-collapsed" in class_list
        except (NoSuchElementException, StaleElementReferenceException):
            continue
    else:
        return False


def expand_row(driver: Driver, idx: int):
    "Expand row at `idx`, first row is idx=2"
    name = driver.waiting(
        f".ant-table-tbody tr:nth-child({idx}) td:nth-child(2)", f"row {idx}"
    ).text
    _logger.info(f"expanding {name}")
    driver.clicking(f".right-content tbody tr:nth-child({idx}) td:nth-child(1) button")


def filter_check_expand_sign(
    driver: Driver,
    name: str,
    chuaky_fn: Callable[[Driver, int], None],
    dangky_fn: Callable[[Driver, int], None],
):
    "filter `name`, expand it if possible, then call `fn` respectively bases on status"

    def check_and_sign(driver: Driver, i: int):
        name = driver.waiting(
            f".ant-table-tbody tr:nth-child({i}) td:nth-child(2)"
        ).text
        _logger.debug(f"checking {name}")
        if is_row(driver, i, Status.CHUAKY):
            _logger.info(f"row condition: not met: {name} -> {Status.CHUAKY}")
            driver.clicking(f"tbody tr:nth-child({i})")
            chuaky_fn(driver, i)
            time.sleep(5)
        elif is_row(driver, i, Status.DANGKY):
            _logger.info(f"row condition: not met: {name} -> {Status.DANGKY}")
            dangky_fn(driver, i)
            time.sleep(5)
        else:
            _logger.info("row condition: OK")

    if filter(driver, name) and (
        driver.waiting(
            ".right-content tbody tr:nth-child(2) td:nth-child(3)"
        ).text.strip()
        != Status.HOANTHANH
    ):
        if is_row_expandable(driver, 2):
            expand_row(driver, 2)
            for i in range(3, len(driver.find_all("tbody .ant-table-row-level-1")) + 3):
                check_and_sign(driver, i)
        else:
            check_and_sign(driver, 2)


def do_nothing():
    "@private"
    _logger.warning("should not be called")


def sign_current(driver: Driver):
    "@private"
    driver.clicking(
        ".right-content .__action button:nth-child(2)", "clicking Ký tên BS dieu tri"
    )


def sign_current2(driver: Driver):
    "@private"
    driver.clicking(
        ".right-content .__action button:nth-child(3)", "clicking Ký tên BS truong khoa"
    )


def sign_current_both(driver: Driver):
    "@private"
    sign_current(driver)
    sign_current2(driver)


def sign_tab(driver: Driver, idx: int, sign_fn: DriverFn):
    "@private"
    tab0 = driver.current_window_handle
    datakey = driver.find(f".ant-table-tbody tr:nth-child({idx})").get_attribute(
        "data-row-key"
    )
    _logger.debug(f"data row key = {datakey}")
    driver.clicking(f".ant-table-tbody tr:nth-child({idx})", f"row {idx - 1}")
    time.sleep(2)
    driver.clicking(f"a[data-key='{datakey}'] button", f"edit button {idx - 1}")
    driver.goto_newtab_do_smth_then_goback(tab0, sign_fn)
