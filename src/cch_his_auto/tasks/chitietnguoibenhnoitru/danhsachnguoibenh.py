"""
### Tasks that operate on *Danh sách người bệnh*
###### inside "*Chi tiết người bệnh nội trú*
"""

import logging
import time

from selenium.webdriver import Keys

from cch_his_auto.driver import Driver

_logger = logging.getLogger()

def open_dialog(driver: Driver):
    driver.clicking(
        ".thong-tin-benh-nhan .bunch-icon div:last-child",
        "xem danh sach nguoi benh",
    )
    driver.waiting(".ant-drawer .searching input", "Danh sách người bệnh")

def close_dialog(driver: Driver):
    driver.clicking(".ant-drawer-mask", "close danh sach nguoi benh")

def filter_patient(driver: Driver, ma_hs: int):
    "After `open_dialog`, filter patient based on `ma_hs`"
    ele = driver.clear_input(".ant-drawer .searching input")
    _logger.info(f"+++++ typing {ma_hs} to search entry")
    ele.send_keys(str(ma_hs))
    ele.send_keys(Keys.ENTER)
    time.sleep(2)
    driver.waiting_to_be(
        "tbody tr:nth-child(2) td:nth-child(3)", str(ma_hs), "patient id"
    )

def goto_patient(driver: Driver, ma_hs: int):
    "After `open_dialog`, filter patient based on `ma_hs`, then open that patient"
    filter_patient(driver, ma_hs)
    driver.clicking("tbody tr:nth-child(2)", "first row")
    driver.waiting_to_be(
        ".patient-information .ant-row span:nth-child(2) b",
        str(ma_hs),
        "patient id",
    )
