"""
### Tasks: đăng ký phục hồi chức năng
"""

import logging
import time

from selenium.common import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver import ActionChains, Keys

from cch_his_auto.driver import Driver

_logger = logging.getLogger().getChild("tasks")

def open_dialog(driver: Driver):
    "Click *Đăng ký PHCN* or *Thêm mới đợt PHCN* button"
    for i in range(20):
        time.sleep(1)
        _logger.debug(f"opening dialog {i}...")
        try:
            ele = driver.waiting(
                ".footer-btn .left button:nth-child(3)", "Đăng ký PHCN"
            )
            if (
                ele.text.strip() == "Đăng ký PHCN"
                or ele.text.strip() == "Thêm mới đợt PHCN"
            ):
                _logger.debug("click open dialog button = Đăng ký PHCN")
                ele.click()
                driver.waiting(".ant-form", "PHCN dialog")
                _logger.info("open Đăng ký PHCN")
            else:
                _logger.debug("PHCN is already registered -> canceling")
                cancel(driver)
        except StaleElementReferenceException:
            _logger.warning("get StaleElementReferenceException")
    else:
        _logger.error("can't open PHCN")
        raise Exception("can't open PHCN")

def cancel(driver: Driver):
    "Click *Hủy đăng ký PHCN* button"
    for i in range(20):
        time.sleep(1)
        _logger.debug(f"canceling registered PHCN {i}...")
        try:
            ele = driver.waiting(
                ".footer-btn .left button:nth-child(3)", "Huỷ đăng ký PHCN"
            )
            if ele.text.strip() == "Hủy đăng ký PHCN":
                _logger.debug("click cancel registered button = Hủy đăng ký PHCN")
                ele.click()
                ele = driver.waiting(
                    ".footer-btn .left button:nth-child(3)", "reset PHCN button"
                )
                if (
                    ele.text.strip() == "Đăng ký PHCN"
                    or ele.text.strip() == "Thêm mới đợt PHCN"
                ):
                    _logger.debug("finish cancel PHCN")
                    return
        except StaleElementReferenceException:
            _logger.warning("get StaleElementReferenceException")
    else:
        _logger.error("can't cancel PHCN")
        raise Exception("can't cancel PHCN")

def clear(driver: Driver):
    "After `open_dialog`, clear all selections"
    _logger.debug("clearing all selections in PHCN dialog")
    for ele in driver.find_all(".ant-form .ant-select-selection-item-remove"):
        _logger.debug(f"removing {ele.text}")
        ele.click()

def drop_menu(driver: Driver):
    "After `open_dialog`, drop down the menu"
    _logger.debug("drop menu")
    driver.waiting(".ant-form .ant-select", "drop menu PHCN").send_keys(Keys.DOWN)

def close_menu(driver: Driver):
    "After `dropmenu`, close the menu"
    _logger.debug("close menu PHCN")
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()

def bunuot(driver: Driver):
    "After `drop_menu`, Add *bú nuốt*"
    driver.clicking(
        ".rc-virtual-list div.ant-select-item-option:nth-child(2)", "add Bú nuốt"
    )
    _logger.info("add Bú nuốt")

def giaotiep(driver: Driver):
    "After `drop_menu`, Add *giao tiếp*"
    driver.clicking(
        ".rc-virtual-list div.ant-select-item-option:nth-child(3)", "add Giao tiếp"
    )
    _logger.info("add Giao tiếp")

def hohap(driver: Driver):
    "After `drop_menu`, Add *hô hấp*"
    driver.clicking(
        ".rc-virtual-list div.ant-select-item-option:nth-child(4)", "add Hô hấp"
    )
    _logger.info("add Hô hấp")

def vandong(driver: Driver):
    "After `drop_menu`, Add *vận động*"
    driver.clicking(
        ".rc-virtual-list div.ant-select-item-option:nth-child(5)", "add Vận động"
    )
    _logger.info("add Vận động")

def save(driver: Driver):
    "Finish and click save"
    driver.clicking(".ant-modal-body .bottom-action-right button", "save button")
    for i in range(20):
        time.sleep(1)
        _logger.debug(f"saving dialog {i}...")
        try:
            ele = driver.find(".footer-btn .left button:nth-child(3)")
            if ele.text.strip() == "Hủy đăng ký PHCN":
                _logger.debug("saved PHCN")
                return
        except (StaleElementReferenceException, NoSuchElementException):
            _logger.warning(
                "get StaleElementReferenceException or NoSuchElementException"
            )
    else:
        _logger.error("can't save PHCN")
        raise Exception("can't save PHCN")
