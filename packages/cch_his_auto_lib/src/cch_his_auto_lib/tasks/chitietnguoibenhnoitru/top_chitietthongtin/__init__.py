import logging
import time
from contextlib import contextmanager

from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.helper import EndOfLoop
from .. import TOP_BTN_CSS

DIALOG_CSS = ".ant-modal:has(.avatar__image)"
_logger = logging.getLogger("top_chitietthongtin")


@contextmanager
def session(driver):
    "use as contextmanager for open and close chitietthongtin dialog"
    try:
        yield open_dialog(driver)
    finally:
        close_dialog(driver)


def open_dialog(driver: Driver):
    driver.clicking(
        f"{TOP_BTN_CSS}>div:first-child",
        "click Chi tiết thông tin button",
    )
    driver.waiting(DIALOG_CSS, "Chi tiết thông tin dialog")


def close_dialog(driver: Driver):
    driver.clicking(
        f"{DIALOG_CSS} .ant-modal-close",
        "close Chi tiết thông tin dialog",
    )
    driver.wait_closing(DIALOG_CSS)


def get_chieucao(driver: Driver) -> str | None:
    for _ in range(30):
        time.sleep(1)
        try:
            value = driver.find(
                f"{DIALOG_CSS} .ant-col:nth-child(5) .ant-row:nth-child(1) .ant-col:nth-child(5) input"
            ).get_attribute("value")
            if value == "":
                continue
            else:
                assert value is not None
                _logger.info(f"-> found chieucao={value}")
                return value
        except NoSuchElementException:
            ...
    else:
        _logger.warning("-> can't found chieucao")
        return None


def get_cannang(driver: Driver) -> str | None:
    for _ in range(30):
        time.sleep(1)
        try:
            value = driver.find(
                f"{DIALOG_CSS} .ant-col:nth-child(5) .ant-row:nth-child(1) .ant-col:nth-child(6) input"
            ).get_attribute("value")
            if value == "":
                continue
            else:
                assert value is not None
                _logger.info(f"-> found cannang={value}")
                return value
        except NoSuchElementException:
            ...
    else:
        _logger.warning("-> can't found cannang")
        return None


def get_age_in_month(driver: Driver) -> int:
    for _ in range(30):
        time.sleep(1)
        try:
            value = driver.find(
                f"{DIALOG_CSS} .ant-col:nth-child(2) .ant-row .ant-col:nth-child(4) input"
            ).get_attribute("value")
            if value == "":
                continue
            else:
                assert value is not None
                _logger.info(f"-> found age={value}")
                a = value.strip().split(" ")
                if len(a) == 1:
                    return int(a[0]) * 12
                if len(a) == 2:
                    if a[1] == "tháng":
                        return int(a[0])
                    else:
                        return 0
                if len(a) == 4:
                    return int(a[0]) * 12 + int(a[2])

        except NoSuchElementException:
            ...
    else:
        _logger.error("-> can't find age")
        raise EndOfLoop("-> can't find age")
