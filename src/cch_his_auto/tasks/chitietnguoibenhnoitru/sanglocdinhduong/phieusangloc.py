import datetime as dt
import time
import logging

from cch_his_auto.driver import Driver
from cch_his_auto.helper import tracing

_logger = logging.getLogger().getChild("phieusangloc")
_trace = tracing(_logger)


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


def back(driver: Driver):
    driver.clicking(".footer-btn .left button", "go back button")
    driver.waiting(".thong-tin-benh-nhan", "chi tiết bệnh nhân")
    time.sleep(5)


@_trace
def save_new_phieusangloc(driver: Driver, date: dt.date, cannang: str, chieucao: str):
    "Complete this *Phiếu sàng lọc* then go back to *Chi tiết bệnh nhân nội trú*"
    _logger.info(f"new phieusangloc: date= {date}")
    set_date(driver, date)
    set_cannang(driver, cannang)
    set_chieucao(driver, chieucao)
    save(driver)
    back(driver)
