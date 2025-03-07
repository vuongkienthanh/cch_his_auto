import logging

from selenium.webdriver import Keys

from cch_his_auto import Driver

logger = logging.getLogger()

def start(driver: Driver):
    ele = driver.waiting(".footer-btn .left button:nth-child(3)")
    if ele.text.strip() == "Đăng ký PHCN" or ele.text.strip() == "Thêm mới đợt PHCN":
        ele.click()
        driver.waiting(".ant-form")

def cancel(driver: Driver):
    ele = driver.waiting(".footer-btn .left button:nth-child(3)")
    if ele.text.strip() == "Hủy đăng ký PHCN":
        ele.click()
        for _ in range(20):
            ele = driver.waiting(".footer-btn .left button:nth-child(3)")
            if (
                ele.text.strip() == "Đăng ký PHCN"
                or ele.text.strip() == "Thêm mới đợt PHCN"
            ):
                break

def clear(driver: Driver):
    for ele in driver.find_all(".ant-form .ant-select-selection-item-remove"):
        ele.click()

def dropmenu(driver: Driver):
    driver.waiting(".ant-form .ant-select").send_keys(Keys.DOWN)

def bunuot(driver: Driver):
    driver.clicking(".rc-virtual-list div.ant-select-item-option:nth-child(2)")

def giaotiep(driver: Driver):
    driver.clicking(".rc-virtual-list div.ant-select-item-option:nth-child(3)")

def hohap(driver: Driver):
    driver.clicking(".rc-virtual-list div.ant-select-item-option:nth-child(4)")

def vandong(driver: Driver):
    driver.clicking(".rc-virtual-list div.ant-select-item-option:nth-child(4)")

def save(driver: Driver):
    driver.clicking(".ant-modal-body .bottom-action-right button")
    for _ in range(20):
        ele = driver.waiting(".footer-btn .left button:nth-child(3)")
        if ele.text.strip() == "Hủy đăng ký PHCN":
            return
    else:
        ele = driver.waiting(".footer-btn .left button:nth-child(3)")
        if (
            ele.text.strip() == "Đăng ký PHCN"
            or ele.text.strip() == "Thêm mới đợt PHCN"
        ):
            logger.error("can't save PHCN")
            raise Exception("can't save PHCN")
