"""
### Tasks: đăng ký phục hồi chức năng
"""

import logging

from selenium.common import StaleElementReferenceException
from selenium.webdriver import ActionChains, Keys

from cch_his_auto import Driver

_logger = logging.getLogger()

def open(driver: Driver):
    "Click *Đăng ký PHCN* or *Thêm mới đợt PHCN* button"
    try:
        ele = driver.waiting(
            ".footer-btn .left button:nth-child(3)", "Nút đăng ký PHCN"
        )
        if (
            ele.text.strip() == "Đăng ký PHCN"
            or ele.text.strip() == "Thêm mới đợt PHCN"
        ):
            ele.click()
            _logger.info("finish open PHCN")
            driver.waiting(".ant-form", "Bảng đăng ký PHCN")
        else:
            cancel(driver)
            open(driver)
    except StaleElementReferenceException:
        open(driver)

def cancel(driver: Driver):
    "Click *Hủy đăng ký PHCN* button"
    try:
        ele = driver.waiting(".footer-btn .left button:nth-child(3)", "Nút huỷ PHCN")
        if ele.text.strip() == "Hủy đăng ký PHCN":
            ele.click()
            ele = driver.waiting(".footer-btn .left button:nth-child(3)")
            if (
                ele.text.strip() == "Đăng ký PHCN"
                or ele.text.strip() == "Thêm mới đợt PHCN"
            ):
                _logger.info("finish cancel PHCN")
            else:
                _logger.error("can't cancel PHCN")
    except StaleElementReferenceException:
        cancel(driver)

def clear(driver: Driver):
    "After `open`, clear all selections"
    _logger.info("clear all selections PHCN")
    for ele in driver.find_all(".ant-form .ant-select-selection-item-remove"):
        ele.click()

def dropmenu(driver: Driver):
    "After `open`, drop down the menu"
    _logger.info("dropmenu PHCN")
    driver.waiting(".ant-form .ant-select").send_keys(Keys.DOWN)

def closemenu(driver: Driver):
    "After `dropmenu`, close the menu"
    _logger.info("closemenu PHCN")
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()

def bunuot(driver: Driver):
    "After `dropmenu`, Add *bú nuốt*"
    _logger.info("add bu nuot")
    driver.clicking(".rc-virtual-list div.ant-select-item-option:nth-child(2)")

def giaotiep(driver: Driver):
    "After `dropmenu`, Add *giao tiếp*"
    _logger.info("add giao tiep")
    driver.clicking(".rc-virtual-list div.ant-select-item-option:nth-child(3)")

def hohap(driver: Driver):
    "After `dropmenu`, Add *hô hấp*"
    _logger.info("add ho hap")
    driver.clicking(".rc-virtual-list div.ant-select-item-option:nth-child(4)")

def vandong(driver: Driver):
    "After `dropmenu`, Add *vận động*"
    _logger.info("add van dong")
    driver.clicking(".rc-virtual-list div.ant-select-item-option:nth-child(5)")

def save(driver: Driver):
    "Finish and click save"
    driver.clicking(".ant-modal-body .bottom-action-right button", "save button")
    for _ in range(20):
        try:
            ele = driver.waiting(".footer-btn .left button:nth-child(3)")
            if ele.text.strip() == "Hủy đăng ký PHCN":
                _logger.info("saved PHCN")
                return
        except StaleElementReferenceException:
            ...
    else:
        _logger.error("can't save PHCN")
        raise Exception("can't save PHCN")
