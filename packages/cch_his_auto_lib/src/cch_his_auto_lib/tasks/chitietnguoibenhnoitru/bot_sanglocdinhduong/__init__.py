import datetime as dt
import time
import logging

from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import Driver

URL = "http://emr.ndtp.org/quan-ly-dinh-duong/phieu-sang-loc/"
_logger = logging.getLogger().getChild("sanglocdinhduong")


def open_dialog(driver: Driver) -> bool:
    "Open *Sàng lọc dinh dưỡng* dialog from *Chi tiết người bệnh nội trú*"
    driver.clicking(
        ".footer-btn .right button:nth-child(1)", "open Sàng lọc dinh dưỡng button"
    )
    try:
        driver.waiting(".ant-modal-body .ant-table", "Sàng lọc dinh dưỡng dialog")
    except NoSuchElementException:
        _logger.info("-> can't find sàng lọc dinh dưỡng dialog")
        if driver.current_url.startswith(URL):
            _logger.info("-> found new phieu sàng lọc dinh dưỡng")
            return False
        else:
            raise Exception("should have a dialog or new phieusangloc")
    else:
        driver.waiting("tbody tr:nth-child(2) td:nth-child(3)")
        _logger.info("-> found sàng lọc dinh dưỡng dialog")
        return True


def close_dialog(driver: Driver):
    "Close *Sàng lọc dinh dưỡng* dialog"
    driver.clicking(
        ".ant-modal-close:has(~.ant-modal-body .ant-table)",
        "close Sàng lọc dinh dưỡng dialog",
    )
    driver.wait_closing(".ant-modal-body .ant-table")


def get_last_date(driver: Driver) -> dt.date:
    "Get last date in *Sàng lọc dinh dưỡng* dialog"
    max_rank = 0
    max_i = 0
    for i in range(2, 12):
        try:
            rank = driver.find(f"tbody tr:nth-child({i}) td:nth-child(3)").text
            if (r := int(rank)) > max_rank:
                max_rank = r
                max_i = i
        except:
            break
    date = dt.datetime.strptime(
        driver.find(f"tbody tr:nth-child({max_i}) td:nth-child(2)").text,
        "%d/%m/%Y %H:%M:%S",
    ).date()
    _logger.info(f"-> found last_date = {date}")
    return date


def add_new(driver: Driver):
    "Add new *Phiếu sàng lọc*, goto `phieusangloc` submodule for more tasks"
    driver.clicking(
        ".ant-modal:has(table) .ant-modal-title button", "add new phiếu sàng lọc"
    )


###################################
# Phiếu sàng lọc
###################################


def back(driver: Driver):
    driver.clicking(".footer-btn .left button", "go back button")
    driver.waiting(".thong-tin-benh-nhan", "chi tiết bệnh nhân")
    time.sleep(5)


def set_date(driver: Driver, date: dt.date):
    driver.clear_input(".input-date").send_keys(date.strftime("%d/%m/%Y"))
    _logger.debug(f"set date to {date}")


def set_cannang(driver: Driver, value: str):
    driver.clear_input("#canNang").send_keys(value)
    _logger.debug(f"set cannang to {value}")


def set_chieucao(driver: Driver, value: str):
    driver.clear_input("#chieuCao").send_keys(value)
    _logger.debug(f"set chieucao to {value}")


def save(driver: Driver):
    driver.clicking(".right button:nth-child(2)", "save phieusangloc")
