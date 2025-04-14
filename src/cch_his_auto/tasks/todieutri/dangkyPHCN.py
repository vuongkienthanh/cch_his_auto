import logging
import time
from enum import StrEnum

from selenium.common import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver import ActionChains, Keys

from cch_his_auto.driver import Driver
from cch_his_auto.helper import tracing, EndOfLoop

_logger = logging.getLogger().getChild("PHCN")
_trace = tracing(_logger)

class _State(StrEnum):
    Register = "Đăng ký PHCN"
    AddNew = "Thêm mới đợt PHCN"
    Cancel = "Hủy đăng ký PHCN"

def _open(driver: Driver):
    driver.clicking(
        ".footer-btn .left button:nth-child(3)", f"{_State.Register} button"
    )
    driver.waiting(".ant-form", "PHCN dialog")

def _cancel(driver: Driver):
    driver.clicking(".footer-btn .left button:nth-child(3)", f"{_State.Cancel} button")
    driver.waiting_to_be(
        ".footer-btn .left button:nth-child(3)",
        _State.AddNew,
        f"{_State.Cancel} becomes {_State.AddNew}",
    )

@_trace
def open_dialog(driver: Driver):
    "Click *Đăng ký PHCN* or *Thêm mới đợt PHCN* button"

    for i in range(120):
        time.sleep(1)
        try:
            _logger.debug(f"checking PHCN button state {i}...")
            ele = driver.waiting(".footer-btn .left button:nth-child(3)", "PHCN button")
            if ele.text.strip() == _State.Register:
                _logger.debug(f"PHCN button state is {_State.Register}")
                _open(driver)
                return
            elif ele.text.strip() == _State.AddNew:
                _logger.debug(f"PHCN button state is {_State.AddNew}")
                _open(driver)
                return
            elif ele.text.strip() == _State.Cancel:
                _logger.debug(f"PHCN button state is {_State.Cancel}")
                _cancel(driver)
                _open(driver)
                return
        except StaleElementReferenceException as e:
            _logger.warning(f"get {e}")
    else:
        raise EndOfLoop("can't open dialog")

@_trace
def cancel(driver: Driver):
    "Click *Hủy đăng ký PHCN* button"

    for i in range(120):
        time.sleep(1)
        try:
            _logger.debug(f"checking PHCN button state {i}...")
            ele = driver.waiting(".footer-btn .left button:nth-child(3)", "PHCN button")
            if ele.text.strip() == _State.Register:
                raise Exception(f"Button state is {_State.Register}")
            elif ele.text.strip() == _State.AddNew:
                raise Exception(f"Button state is {_State.AddNew}")
            elif ele.text.strip() == _State.Cancel:
                _logger.debug(f"PHCN button state is {_State.Cancel}")
                _cancel(driver)
                return
        except StaleElementReferenceException as e:
            _logger.warning(f"get {e}")
    else:
        raise EndOfLoop("can't cancel PHCN")

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
    "Finish and click save dialog"
    driver.clicking(".ant-modal-body .bottom-action-right button", "save button")
    for i in range(120):
        time.sleep(1)
        try:
            _logger.debug(f"checking PHCN button state {i}...")
            ele = driver.find(".footer-btn .left button:nth-child(3)")
            if ele.text.strip() == _State.Cancel:
                _logger.debug(f"PHCN button state is {_State.Cancel}")
                return
        except (StaleElementReferenceException, NoSuchElementException) as e:
            _logger.warning(f"get {e}")
    else:
        raise EndOfLoop("can't save PHCN dialog")
