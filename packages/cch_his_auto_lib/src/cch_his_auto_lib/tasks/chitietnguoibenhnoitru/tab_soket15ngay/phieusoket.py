import time
import datetime as dt
from cch_his_auto_lib.driver import Driver
from . import _logger, _trace


def back(driver: Driver):
    driver.clicking(".footer-btn .left button", "go back button")
    driver.waiting(".thong-tin-benh-nhan", "chi tiết bệnh nhân")
    time.sleep(5)


def save(driver: Driver):
    driver.clicking(".footer-btn .right button", "save phieusoket")


def set_start_date(driver: Driver, date: dt.date):
    driver.clear_input(".content .title .left .date:first-of-type input").send_keys(
        date.strftime("%d/%m/%Y")
    )
    _logger.debug(f"set start date to {date}")


def set_end_date(driver: Driver, date: dt.date):
    driver.clear_input(".content .title .left .date:last-of-type input").send_keys(
        date.strftime("%d/%m/%Y")
    )
    _logger.debug(f"set end date to {date}")


def set_dienbien(driver: Driver, value: str):
    driver.clear_input(".content .info .ant-col:nth-child(4) textarea").send_keys(value)
    _logger.debug(f"set dienbien to {value}")


def set_dieutri(driver: Driver, value: str):
    driver.clear_input(".content .info .ant-col:nth-child(6) textarea").send_keys(value)
    _logger.debug(f"set dieutri to {value}")


def set_ketqua(driver: Driver, value: str):
    driver.clear_input(".content .info .ant-col:nth-child(7) textarea").send_keys(value)
    _logger.debug(f"set ketqua to {value}")


def set_tienluong(driver: Driver, value: str):
    driver.clear_input(".content .info .ant-col:nth-child(8) textarea").send_keys(value)
    _logger.debug(f"set tienluong to {value}")


@_trace
def save_new_phieusoket(
    driver: Driver,
    start_date: dt.date,
    end_date: dt.date,
    dienbien: str,
    dieutri: str,
    ketqua: str,
    tienluong: str,
):
    "Complete this *Phiếu sơ kết* then go back"
    _logger.info(f"new phieusoket: start_date= {start_date}, end_date= {end_date}")
    set_dienbien(driver, dienbien)
    set_dieutri(driver, dieutri)
    set_ketqua(driver, ketqua)
    set_tienluong(driver, tienluong)
    save(driver)
    back(driver)
