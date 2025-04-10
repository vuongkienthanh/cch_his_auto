"""
### Tasks that operate on *Sàng lọc dinh dưỡng*
###### inside "*Chi tiết người bệnh nội trú*
"""

import time
import datetime as dt

from cch_his_auto.driver import Driver

def open_dialog(driver: Driver):
    driver.clicking(
        ".footer-btn .right button:nth-child(1)", "open Sàng lọc dinh dưỡng"
    )
    driver.waiting(".ant-modal-body .ant-table", "Sàng lọc dinh dưỡng dialog")
    time.sleep(2)

def close_dialog(driver: Driver):
    driver.clicking(
        ".ant-modal-close:has(~.ant-modal-body .ant-table)",
        "close Sàng lọc dinh dưỡng dialog",
    )
    time.sleep(2)

def get_last_date(driver: Driver, admission_date: dt.date) -> dt.date:
    try:
        return dt.datetime.strptime(
            driver.find("tbody tr:nth-child(2) td:nth-child(2)").text,
            "%d/%m/%Y %H:%M:%S",
        ).date()
    except:
        return admission_date

def add_new(driver:Driver):
    driver.clicking(".ant-modal:has(table) .ant-modal-title button")
