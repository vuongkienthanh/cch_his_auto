"""
### Tasks that operate on *Sàng lọc dinh dưỡng*
###### inside "*Chi tiết người bệnh nội trú*
"""

URL = "http://emr.ndtp.org/quan-ly-dinh-duong/phieu-sang-loc/"
"All tasks in this submodule work under this url."

import datetime as dt
import logging
import time


from cch_his_auto.driver import Driver
from cch_his_auto.tasks.chitietnguoibenhnoitru import get_admission_date
from cch_his_auto.tasks.chitietnguoibenhnoitru import chitietthongtin as cttt
from .phieusangloc import save_new_phieusangloc

_logger = logging.getLogger()

def open_dialog(driver: Driver):
    driver.clicking(
        ".footer-btn .right button:nth-child(1)", "open Sàng lọc dinh dưỡng"
    )
    driver.waiting(".ant-modal-body .ant-table", "Sàng lọc dinh dưỡng dialog")

def close_dialog(driver: Driver):
    driver.clicking(
        ".ant-modal-close:has(~.ant-modal-body .ant-table)",
        "close Sàng lọc dinh dưỡng dialog",
    )
    time.sleep(5)

def get_last_date(driver: Driver) -> dt.date | None:
    try:
        last_date = dt.datetime.strptime(
            driver.find("tbody tr:nth-child(2) td:nth-child(2)").text,
            "%d/%m/%Y %H:%M:%S",
        ).date()
        _logger.info(f"found last_date = {last_date}")
        return last_date
    except:
        _logger.warning("last_date not found")
        return None

def add_new(driver: Driver):
    driver.clicking(
        ".ant-modal:has(table) .ant-modal-title button", "add new phiếu sàng lọc"
    )

def complete_sanglocdinhduong(driver: Driver):
    "complete all phieusangloc from admission_date up til today"
    admission_date = get_admission_date(driver)
    cttt.open_dialog(driver)
    cannang = cttt.get_cannang(driver)
    chieucao = cttt.get_chieucao(driver)
    cttt.close_dialog(driver)
    if (cannang == "") or (chieucao == "") or (cannang is None) or (chieucao is None):
        _logger.warning("cannang or chieucao is empty")
        return
    open_dialog(driver)
    if last_date := get_last_date(driver):
        next_date = last_date + dt.timedelta(days=7)
    else:
        next_date = admission_date

    today = dt.date.today()

    while next_date <= today:
        add_new(driver)
        save_new_phieusangloc(driver, next_date, cannang, chieucao)
        next_date = next_date + dt.timedelta(days=7)
        open_dialog(driver)

    close_dialog(driver)
