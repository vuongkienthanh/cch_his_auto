import time
import datetime as dt

from cch_his_auto_lib.driver import get_global_driver
from . import _lgr, _trace


def back():
    _d = get_global_driver()
    _d.clicking(".footer-btn .left button", "go back button")
    _d.waiting(".thong-tin-benh-nhan", "chi tiết bệnh nhân")
    time.sleep(5)


def set_date(date: dt.date):
    _d = get_global_driver()
    _d.clear_input(".input-date").send_keys(date.strftime("%d/%m/%Y"))
    _lgr.debug(f"set date to {date}")


def set_cannang(value: str):
    _d = get_global_driver()
    _d.clear_input("#canNang").send_keys(value)
    _lgr.debug(f"set cannang to {value}")


def set_chieucao(value: str):
    _d = get_global_driver()
    _d.clear_input("#chieuCao").send_keys(value)
    _lgr.debug(f"set chieucao to {value}")


def set_machedo(value: str):
    _d = get_global_driver()
    _d.clear_input("#dsDuongNuoiAn>.ant-row>.ant-col:last-child>div>input").send_keys(
        value
    )
    _lgr.debug(f"set machedo to {value}")


def save():
    _d = get_global_driver()
    _d.clicking(".footer-btn .right button:nth-child(2)", "save phieusangloc")


@_trace
def save_new_phieusangloc(date: dt.date, cannang: str, chieucao: str, machedo: str):
    "Complete this *Phiếu sàng lọc* then go back"
    _lgr.info(f"new phieusangloc: date= {date}")
    set_date(date)
    set_cannang(cannang)
    set_chieucao(chieucao)
    set_machedo(machedo)
    save()
    back()
