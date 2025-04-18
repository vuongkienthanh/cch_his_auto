import datetime as dt
import logging
import time

from selenium.common import NoSuchElementException

from cch_his_auto.driver import Driver
from cch_his_auto.helper import EndOfLoop, tracing
from cch_his_auto.tasks.chitietnguoibenhnoitru import get_admission_date
from cch_his_auto.tasks.chitietnguoibenhnoitru import chitietthongtin as cttt
from .phieusangloc import save_new_phieusangloc

URL = "http://emr.ndtp.org/quan-ly-dinh-duong/phieu-sang-loc/"
_logger = logging.getLogger().getChild("sanglocdinhduong")
_trace = tracing(_logger)


@_trace
def open_dialog(driver: Driver) -> bool:
    "Open *Sàng lọc dinh dưỡng* dialog from *Chi tiết người bệnh nội trú*"
    driver.clicking(
        ".footer-btn .right button:nth-child(1)", "open Sàng lọc dinh dưỡng button"
    )
    try:
        driver.waiting(".ant-modal-body .ant-table", "Sàng lọc dinh dưỡng dialog")
    except NoSuchElementException:
        if driver.current_url.startswith(
            "http://emr.ndtp.org/quan-ly-dinh-duong/phieu-sang-loc/"
        ):
            return False
        else:
            raise Exception("should have a dialog or new phieusangloc")
    else:
        return True


@_trace
def close_dialog(driver: Driver):
    "Close *Sàng lọc dinh dưỡng* dialog"
    driver.clicking(
        ".ant-modal-close:has(~.ant-modal-body .ant-table)",
        "close Sàng lọc dinh dưỡng dialog",
    )
    time.sleep(3)


def get_last_date(driver: Driver) -> dt.date:
    "Get last date in *Sàng lọc dinh dưỡng* dialog"
    date = dt.datetime.strptime(
        driver.find("tbody tr:nth-child(2) td:nth-child(2)").text,
        "%d/%m/%Y %H:%M:%S",
    ).date()
    _logger.debug(f"-> found last_date = {date}")
    return date


def add_new(driver: Driver):
    "Add new *Phiếu sàng lọc*, goto `phieusangloc` submodule for more tasks"
    driver.clicking(
        ".ant-modal:has(table) .ant-modal-title button", "add new phiếu sàng lọc"
    )


@_trace
def complete_sanglocdinhduong(driver: Driver):
    "Complete all *Phiếu sàng lọc* from admission_date up til today"
    admission_date = get_admission_date(driver)
    cttt.open_dialog(driver)
    cannang = cttt.get_cannang(driver)
    chieucao = cttt.get_chieucao(driver)
    cttt.close_dialog(driver)
    if (cannang == "") or (chieucao == "") or (cannang is None) or (chieucao is None):
        _logger.warning("cannang or chieucao is empty -> skip Sàng lọc dinh dưỡng")
        return

    today = dt.date.today()

    if open_dialog(driver):
        next_date = get_last_date(driver) + dt.timedelta(days=7)
        add_new(driver)
    else:
        next_date = admission_date

    save_new_phieusangloc(driver, next_date, cannang, chieucao)
    next_date = next_date + dt.timedelta(days=7)

    while next_date <= today:
        open_dialog(driver)
        add_new(driver)
        save_new_phieusangloc(driver, next_date, cannang, chieucao)
        next_date = next_date + dt.timedelta(days=7)
