"""
### Tasks: đăng ký phục hồi chức năng
"""

import logging
import time
from enum import StrEnum

from selenium.common import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver import ActionChains, Keys

from cch_his_auto.driver import Driver
from cch_his_auto.helper import tracing

_logger = logging.getLogger().getChild("tasks.dangkyPHCN")
_trace = tracing(_logger)

class ButtonState(StrEnum):
    Register = "Đăng ký PHCN"
    AddNew = "Thêm mới đợt PHCN"
    Cancel = "Hủy đăng ký PHCN"

@_trace
def open_dialog(driver: Driver):
    "Click *Đăng ký PHCN* or *Thêm mới đợt PHCN* button"

    def _open():
        driver.clicking(".footer-btn .left button:nth-child(3)", "Đăng ký PHCN")
        driver.waiting(".ant-form", "PHCN dialog")

    for i in range(120):
        time.sleep(1)
        try:
            _logger.debug(f"checking PHCN button state {i}...")
            ele = driver.waiting(
                ".footer-btn .left button:nth-child(3)", "Đăng ký PHCN"
            )
            if ele.text.strip() == ButtonState.Register:
                _logger.debug(f"PHCN button state is {ButtonState.Register}")
                _open()
                return
            elif ele.text.strip() == ButtonState.AddNew:
                _logger.debug(f"PHCN button state is {ButtonState.AddNew}")
                _open()
                return
            elif ele.text.strip() == ButtonState.Cancel:
                _logger.debug(f"PHCN button state is {ButtonState.Cancel}")
                cancel(driver)
                _open()
                return
        except StaleElementReferenceException:
            _logger.warning("get StaleElementReferenceException")
    else:
        raise Exception("end of checking loop")

@_trace
def cancel(driver: Driver):
    "Click *Hủy đăng ký PHCN* button"

    for i in range(120):
        time.sleep(1)
        try:
            _logger.debug(f"checking PHCN button state {i}...")
            ele = driver.waiting(
                ".footer-btn .left button:nth-child(3)", "Huỷ đăng ký PHCN"
            )
            if ele.text.strip() == ButtonState.Cancel:
                _logger.debug(f"PHCN button state is {ButtonState.Cancel}")
                ele.click()
                time.sleep(5)
                return
        except StaleElementReferenceException:
            _logger.warning("get StaleElementReferenceException")
    else:
        raise Exception("end of checking loop")

@_trace
def clear(driver: Driver):
    "After `open_dialog`, clear all selections"
    for ele in driver.find_all(".ant-form .ant-select-selection-item-remove"):
        _logger.debug(f"removing {ele.text}")
        ele.click()

@_trace
def drop_menu(driver: Driver):
    "After `open_dialog`, drop down the menu"
    driver.waiting(".ant-form .ant-select", "drop menu PHCN").send_keys(Keys.DOWN)

@_trace
def close_menu(driver: Driver):
    "After `dropmenu`, close the menu"
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()

@_trace
def add_bunuot(driver: Driver):
    "After `drop_menu`, Add *bú nuốt*"
    driver.clicking(
        ".rc-virtual-list div.ant-select-item-option:nth-child(2)", "add Bú nuốt"
    )

@_trace
def add_giaotiep(driver: Driver):
    "After `drop_menu`, Add *giao tiếp*"
    driver.clicking(
        ".rc-virtual-list div.ant-select-item-option:nth-child(3)", "add Giao tiếp"
    )

@_trace
def add_hohap(driver: Driver):
    "After `drop_menu`, Add *hô hấp*"
    driver.clicking(
        ".rc-virtual-list div.ant-select-item-option:nth-child(4)", "add Hô hấp"
    )

@_trace
def add_vandong(driver: Driver):
    "After `drop_menu`, Add *vận động*"
    driver.clicking(
        ".rc-virtual-list div.ant-select-item-option:nth-child(5)", "add Vận động"
    )

@_trace
def save(driver: Driver):
    "Finish and click save"
    driver.clicking(".ant-modal-body .bottom-action-right button", "save button")
    for i in range(120):
        time.sleep(1)
        _logger.debug(f"checking PHCN button state {i}...")
        try:
            ele = driver.find(".footer-btn .left button:nth-child(3)")
            if ele.text.strip() == ButtonState.Cancel:
                return
        except (StaleElementReferenceException, NoSuchElementException):
            _logger.warning(
                "get StaleElementReferenceException or NoSuchElementException"
            )
    else:
        raise Exception("end of checking loop")
