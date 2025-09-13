import datetime as dt

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.action import top_patient_info
from . import _lgr, _trace


def back(d: Driver):
    d.clicking(".footer-btn .left button", "go back button")
    top_patient_info.wait_loaded(d)


def set_date(d: Driver, date: dt.date):
    d.clear_input(".input-date").send_keys(date.strftime("%d/%m/%Y"))
    _lgr.debug(f"set date to {date}")


def get_cannang(d: Driver) -> str | None:
    return d.waiting("#canNang").get_attribute("value")


def get_chieucao(d: Driver) -> str | None:
    return d.waiting("#chieuCao").get_attribute("value")


def set_cannang(d: Driver, value: str):
    d.clear_input("#canNang").send_keys(value)
    _lgr.debug(f"set cannang to {value}")


def set_chieucao(d: Driver, value: str):
    d.clear_input("#chieuCao").send_keys(value)
    _lgr.debug(f"set chieucao to {value}")


def set_machedo(d: Driver, value: str):
    d.clicking("#dsDuongNuoiAn>.ant-row>.ant-col:last-child>div>label span")
    d.clear_input("#dsDuongNuoiAn>.ant-row>.ant-col:last-child>div>input").send_keys(
        value
    )
    _lgr.debug(f"set machedo to {value}")


def save(d: Driver):
    d.clicking(".footer-btn .right button:nth-child(2)", "save phieusangloc")


@_trace
def save_new_phieusangloc(
    d: Driver, date: dt.date, cannang: str, chieucao: str, machedo: str
):
    "Complete this *Phiếu sàng lọc* then go back"
    _lgr.info(f"new phieusangloc: date= {date}")
    top_patient_info.wait_loaded(d)
    set_date(d, date)
    set_cannang(d, cannang)
    set_chieucao(d, chieucao)
    set_machedo(d, machedo)
    save(d)
    back(d)
