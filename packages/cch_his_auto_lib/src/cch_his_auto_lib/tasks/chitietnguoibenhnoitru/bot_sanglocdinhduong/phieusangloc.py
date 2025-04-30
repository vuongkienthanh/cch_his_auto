import time
import datetime as dt
from cch_his_auto_lib.driver import Driver
from . import _logger, _trace


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


def set_machedo(driver: Driver, value: str):
    driver.clear_input(
        "#dsDuongNuoiAn>.ant-row>.ant-col:last-child>div>input"
    ).send_keys(value)
    _logger.debug(f"set machedo to {value}")


def save(driver: Driver):
    driver.clicking(".footer-btn .right button:nth-child(2)", "save phieusangloc")


@_trace
def save_new_phieusangloc(
    driver: Driver, date: dt.date, cannang: str, chieucao: str, machedo: str
):
    "Complete this *Phiếu sàng lọc* then go back"
    _logger.info(f"new phieusangloc: date= {date}")
    set_date(driver, date)
    set_cannang(driver, cannang)
    set_chieucao(driver, chieucao)
    set_machedo(driver, machedo)
    save(driver)
    back(driver)
