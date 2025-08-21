import datetime as dt
import logging

from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tracing import tracing
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru import (
    top_chitietthongtin,
)

URL = "http://emr.ndtp.org/quan-ly-dinh-duong/phieu-sang-loc/"

_lgr = logging.getLogger("bot_sanglocdinhduong")
_trace = tracing(_lgr)

from .helper import build_machedo
from .phieusangloc import save_new_phieusangloc


def open_dialog(d: Driver) -> bool:
    "Open *Sàng lọc dinh dưỡng* dialog from *Chi tiết người bệnh nội trú*"
    d.clicking(
        ".footer-btn .right button:nth-child(1)", "open Sàng lọc dinh dưỡng button"
    )
    try:
        d.waiting(".ant-modal-body .ant-table", "Sàng lọc dinh dưỡng dialog")
    except NoSuchElementException:
        _lgr.info("-> can't find sàng lọc dinh dưỡng dialog")
        if d.current_url.startswith(URL):
            _lgr.info("-> found new phieu sàng lọc dinh dưỡng")
            return False
        else:
            raise Exception("should have a dialog or new phieusangloc")
    else:
        d.waiting("tbody tr:nth-child(2) td:nth-child(3)")
        _lgr.info("-> found sàng lọc dinh dưỡng dialog")
        return True


def close_dialog(d: Driver):
    "Close *Sàng lọc dinh dưỡng* dialog"
    d.clicking(
        ".ant-modal-close:has(~.ant-modal-body .ant-table)",
        "close Sàng lọc dinh dưỡng dialog",
    )
    d.wait_closing(".ant-modal-body .ant-table")


def get_last_date(d: Driver) -> dt.date:
    "Get last date in *Sàng lọc dinh dưỡng* dialog"
    max_rank = 0
    max_i = 0
    for i in range(2, 12):
        try:
            rank = d.find(f"tbody tr:nth-child({i}) td:nth-child(3)").text
            if (r := int(rank)) > max_rank:
                max_rank = r
                max_i = i
        except:
            break
    date = dt.datetime.strptime(
        d.find(f"tbody tr:nth-child({max_i}) td:nth-child(2)").text,
        "%d/%m/%Y %H:%M:%S",
    ).date()
    _lgr.info(f"-> found last_date = {date}")
    return date


def add_new(d: Driver):
    "Add new *Phiếu sàng lọc*"
    d.clicking(
        ".ant-modal:has(table) .ant-modal-title button", "add new phiếu sàng lọc"
    )


@_trace
def add_all_phieusanglocdinhduong(d: Driver, admission_date: dt.date):
    "Complete all *Phiếu sàng lọc* from admission_date up til today"
    with top_chitietthongtin.session():
        cannang = top_chitietthongtin.get_cannang()
        age_in_month = top_chitietthongtin.get_age_in_month()
        if not cannang:
            _lgr.warning("cannang is empty -> skip Sàng lọc dinh dưỡng")
            return
        chieucao = top_chitietthongtin.get_chieucao()
        if not chieucao:
            _lgr.warning("chieucao is empty -> skip Sàng lọc dinh dưỡng")
            return

    today = dt.date.today()

    if open_dialog(d):
        next_date = get_last_date(d) + dt.timedelta(days=7)
        if next_date <= today:
            _lgr.info(f"add new phieu sang loc for {next_date}")
            add_new(d)
        else:
            close_dialog(d)
            return
    else:
        next_date = admission_date

    save_new_phieusangloc(d, next_date, cannang, chieucao, build_machedo(age_in_month))
    next_date = next_date + dt.timedelta(days=7)

    while next_date <= today:
        _lgr.info(f"add new phieu sang loc for {next_date}")
        open_dialog(d)
        add_new(d)
        save_new_phieusangloc(
            d,
            next_date,
            cannang,
            chieucao,
            build_machedo(age_in_month),
        )
        next_date = next_date + dt.timedelta(days=7)
