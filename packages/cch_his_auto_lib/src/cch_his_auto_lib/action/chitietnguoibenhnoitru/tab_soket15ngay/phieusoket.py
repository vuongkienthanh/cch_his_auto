import time
import datetime as dt

from cch_his_auto_lib.driver import Driver
from . import _lgr, _trace


def back(d: Driver):
    d.clicking(".footer-btn .left button", "go back button")
    d.waiting(".thong-tin-benh-nhan", "chi tiết bệnh nhân")
    time.sleep(5)


def save(d: Driver):
    d.clicking(".footer-btn .right button", "save phieusoket")


def set_start_date(d: Driver, date: dt.date):
    d.clear_input(".content .title .left .date:first-of-type input").send_keys(
        date.strftime("%d/%m/%Y")
    )
    _lgr.debug(f"set start date to {date}")


def set_end_date(d: Driver, date: dt.date):
    d.clear_input(".content .title .left .date:last-of-type input").send_keys(
        date.strftime("%d/%m/%Y")
    )
    _lgr.debug(f"set end date to {date}")


def set_dienbien(d: Driver, value: str):
    d.clear_input(".content .info .ant-col:nth-child(4) textarea").send_keys(value)
    _lgr.debug(f"set dienbien to {value}")


def set_dieutri(d: Driver, value: str):
    d.clear_input(".content .info .ant-col:nth-child(6) textarea").send_keys(value)
    _lgr.debug(f"set dieutri to {value}")


def set_ketqua(d: Driver, value: str):
    d.clear_input(".content .info .ant-col:nth-child(7) textarea").send_keys(value)
    _lgr.debug(f"set ketqua to {value}")


def set_tienluong(d: Driver, value: str):
    d.clear_input(".content .info .ant-col:nth-child(8) textarea").send_keys(value)
    _lgr.debug(f"set tienluong to {value}")


@_trace
def save_new_phieusoket(
    d: Driver,
    start_date: dt.date,
    end_date: dt.date,
    dienbien: str,
    dieutri: str,
    ketqua: str,
    tienluong: str,
):
    "Complete this *Phiếu sơ kết* then go back"
    _lgr.info(f"new phieusoket: start_date= {start_date}, end_date= {end_date}")
    set_dienbien(d, dienbien)
    set_dieutri(d, dieutri)
    set_ketqua(d, ketqua)
    set_tienluong(d, tienluong)
    save(d)
    back(d)
