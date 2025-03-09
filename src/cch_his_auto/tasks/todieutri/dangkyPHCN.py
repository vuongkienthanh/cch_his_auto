"""
### Tasks: đăng ký phục hồi chức năng
"""

import logging

from selenium.webdriver import Keys

from cch_his_auto import Driver

_logger = logging.getLogger()

def open(driver: Driver):
    "Click *Đăng ký PHCN* or *Thêm mới đợt PHCN* button"
    ele = driver.waiting(".footer-btn .left button:nth-child(3)","Nút đăng ký PHCN")
    if ele.text.strip() == "Đăng ký PHCN" or ele.text.strip() == "Thêm mới đợt PHCN":
        ele.click()
        _logger.info("finish open PHCN")
        driver.waiting(".ant-form", "Bảng đăng ký PHCN")

def cancel(driver: Driver):
    "Click *Hủy đăng ký PHCN* button"
    ele = driver.waiting(".footer-btn .left button:nth-child(3)", "Nút huỷ PHCN")
    if ele.text.strip() == "Hủy đăng ký PHCN":
        ele.click()
        for _ in range(20):
            ele = driver.waiting(".footer-btn .left button:nth-child(3)")
            if (
                ele.text.strip() == "Đăng ký PHCN"
                or ele.text.strip() == "Thêm mới đợt PHCN"
            ):
                _logger.info("finish cancel PHCN")
                break

def clear(driver: Driver):
    "After `open`, clear all selections"
    _logger.info("clear all selections PHCN")
    for ele in driver.find_all(".ant-form .ant-select-selection-item-remove"):
        ele.click()

def dropmenu(driver: Driver):
    "After `open`, drop down the menu"
    _logger.info("dropmenu PHCN")
    driver.waiting(".ant-form .ant-select").send_keys(Keys.DOWN)

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
    _logger.info("add ho hap")
    _logger.info("add van dong")
    driver.clicking(".rc-virtual-list div.ant-select-item-option:nth-child(4)")

def save(driver: Driver):
    "Finish and click save"
    driver.clicking(".ant-modal-body .bottom-action-right button")
    for _ in range(20):
        ele = driver.waiting(".footer-btn .left button:nth-child(3)")
        if ele.text.strip() == "Hủy đăng ký PHCN":
            _logger.info("saved PHCN")
            return
    else:
        ele = driver.waiting(".footer-btn .left button:nth-child(3)")
        if (
            ele.text.strip() == "Đăng ký PHCN"
            or ele.text.strip() == "Thêm mới đợt PHCN"
        ):
            _logger.error("can't save PHCN")
            raise Exception("can't save PHCN")
