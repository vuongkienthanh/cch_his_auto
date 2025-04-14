"""
### Tasks: đăng ký phục hồi chức năng
"""

import logging

from selenium.common import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver import ActionChains, Keys

from cch_his_auto.driver import Driver

_logger = logging.getLogger()

def open_dialog(driver: Driver):
    "Click *Đăng ký PHCN* or *Thêm mới đợt PHCN* button"
    for _ in range(20):
        try:
            ele = driver.waiting(
                ".footer-btn .left button:nth-child(3)", "Đăng ký PHCN"
            )
            if (
                ele.text.strip() == "Đăng ký PHCN"
                or ele.text.strip() == "Thêm mới đợt PHCN"
            ):
                ele.click()
                driver.waiting(".ant-form", "PHCN dialog")
            else:
                _logger.info("PHCN is already registered -> canceling")
                cancel(driver)
        except StaleElementReferenceException:
            ...
    else:
        _logger.error("can't open PHCN")
        raise Exception("can't open PHCN")

def cancel(driver: Driver):
    "Click *Hủy đăng ký PHCN* button"
    for _ in range(20):
        try:
            ele = driver.waiting(
                ".footer-btn .left button:nth-child(3)", "Huỷ đăng ký PHCN"
            )
            if ele.text.strip() == "Hủy đăng ký PHCN":
                ele.click()
                ele = driver.waiting(
                    ".footer-btn .left button:nth-child(3)", "reset PHCN button"
                )
                if (
                    ele.text.strip() == "Đăng ký PHCN"
                    or ele.text.strip() == "Thêm mới đợt PHCN"
                ):
                    _logger.info("finish cancel PHCN")
        except StaleElementReferenceException:
            ...
    else:
        _logger.error("can't cancel PHCN")
        raise Exception("can't cancel PHCN")

def clear(driver: Driver):
    "After `open_dialog`, clear all selections"
    _logger.info("clear all selections in PHCN dialog")
    for ele in driver.find_all(".ant-form .ant-select-selection-item-remove"):
        ele.click()

def drop_menu(driver: Driver):
    "After `open_dialog`, drop down the menu"
    driver.waiting(".ant-form .ant-select", "drop menu PHCN").send_keys(Keys.DOWN)

def close_menu(driver: Driver):
    "After `dropmenu`, close the menu"
    _logger.info("close menu PHCN")
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()

def bunuot(driver: Driver):
    "After `drop_menu`, Add *bú nuốt*"
    _logger.info("add bu nuot")
    driver.clicking(
        ".rc-virtual-list div.ant-select-item-option:nth-child(2)", "add Bú nuốt"
    )

def giaotiep(driver: Driver):
    "After `drop_menu`, Add *giao tiếp*"
    driver.clicking(
        ".rc-virtual-list div.ant-select-item-option:nth-child(3)", "add Giao tiếp"
    )

def hohap(driver: Driver):
    "After `drop_menu`, Add *hô hấp*"
    driver.clicking(
        ".rc-virtual-list div.ant-select-item-option:nth-child(4)", "add Hô hấp"
    )

def vandong(driver: Driver):
    "After `drop_menu`, Add *vận động*"
    driver.clicking(
        ".rc-virtual-list div.ant-select-item-option:nth-child(5)", "add Vận động"
    )

def save(driver: Driver):
    "Finish and click save"
    driver.clicking(".ant-modal-body .bottom-action-right button", "save button")
    for _ in range(20):
        try:
            ele = driver.find(".footer-btn .left button:nth-child(3)")
            if ele.text.strip() == "Hủy đăng ký PHCN":
                _logger.info("saved PHCN")
                return
        except (StaleElementReferenceException, NoSuchElementException):
            ...
    else:
        _logger.error("can't save PHCN")
        raise Exception("can't save PHCN")
