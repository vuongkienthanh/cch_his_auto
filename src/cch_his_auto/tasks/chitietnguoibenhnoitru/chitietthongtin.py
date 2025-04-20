import logging
import time

from selenium.common import NoSuchElementException

from cch_his_auto.driver import Driver
from cch_his_auto.helper import tracing

_logger = logging.getLogger().getChild("chitietthongtin")
_trace = tracing(_logger)


@_trace
def open_dialog(driver: Driver):
    driver.clicking(
        ".thong-tin-benh-nhan .bunch-icon div:first-child",
        "click Chi tiết thông tin button",
    )
    driver.waiting(".avatar__image", "Chi tiết thông tin dialog")


@_trace
def close_dialog(driver: Driver):
    driver.clicking(
        ".ant-modal-close:has(~.ant-modal-body .avatar__image)",
        "close Chi tiết thông tin dialog",
    )
    driver.wait_closing(".ant-modal-body .avatar__image")


def get_chieucao(driver: Driver) -> str | None:
    for _ in range(30):
        time.sleep(1)
        try:
            value = driver.find(
                ".ant-modal:has( .avatar__image) div:nth-child(5) .ant-row div:nth-child(5) input"
            ).get_attribute("value")
            if value == "" :
                continue
            else:
                _logger.info(f"-> found chieucao={value}")
                return value
        except NoSuchElementException:
            _logger.debug("-> can't find chieucao")
    else:
        return None


def get_cannang(driver: Driver) -> str | None:
    for _ in range(30):
        time.sleep(1)
        try:
            value = driver.find(
                ".ant-modal:has( .avatar__image) div:nth-child(5) .ant-row div:nth-child(6) input"
            ).get_attribute("value")
            if value == "" :
                continue
            else:
                _logger.info(f"-> found cannang={value}")
                return value
        except NoSuchElementException:
            _logger.debug("-> can't find cannang")
    else:
        return None
