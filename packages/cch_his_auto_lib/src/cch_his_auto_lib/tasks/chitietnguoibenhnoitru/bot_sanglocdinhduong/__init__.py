import datetime as dt
import logging

from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import get_global_driver
from cch_his_auto_lib.helper import tracing
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru import (
    top_chitietthongtin,
)

URL = "http://emr.ndtp.org/quan-ly-dinh-duong/phieu-sang-loc/"

_lgr = logging.getLogger("bot_sanglocdinhduong")
_trace = tracing(_lgr)

from .helper import build_machedo
from .phieusangloc import save_new_phieusangloc


def open_dialog() -> bool:
    "Open *Sàng lọc dinh dưỡng* dialog from *Chi tiết người bệnh nội trú*"
    _d = get_global_driver()
    _d.clicking(
        ".footer-btn .right button:nth-child(1)", "open Sàng lọc dinh dưỡng button"
    )
    try:
        _d.waiting(".ant-modal-body .ant-table", "Sàng lọc dinh dưỡng dialog")
    except NoSuchElementException:
        _lgr.info("-> can't find sàng lọc dinh dưỡng dialog")
        if _d.current_url.startswith(URL):
            _lgr.info("-> found new phieu sàng lọc dinh dưỡng")
            return False
        else:
            raise Exception("should have a dialog or new phieusangloc")
    else:
        _d.waiting("tbody tr:nth-child(2) td:nth-child(3)")
        _lgr.info("-> found sàng lọc dinh dưỡng dialog")
        return True


def close_dialog():
    "Close *Sàng lọc dinh dưỡng* dialog"
    _d = get_global_driver()
    _d.clicking(
        ".ant-modal-close:has(~.ant-modal-body .ant-table)",
        "close Sàng lọc dinh dưỡng dialog",
    )
    _d.wait_closing(".ant-modal-body .ant-table")


def get_last_date() -> dt.date:
    "Get last date in *Sàng lọc dinh dưỡng* dialog"
    _d = get_global_driver()
    max_rank = 0
    max_i = 0
    for i in range(2, 12):
        try:
            rank = _d.find(f"tbody tr:nth-child({i}) td:nth-child(3)").text
            if (r := int(rank)) > max_rank:
                max_rank = r
                max_i = i
        except:
            break
    date = dt.datetime.strptime(
        _d.find(f"tbody tr:nth-child({max_i}) td:nth-child(2)").text,
        "%d/%m/%Y %H:%M:%S",
    ).date()
    _lgr.info(f"-> found last_date = {date}")
    return date


def add_new():
    "Add new *Phiếu sàng lọc*"
    _d = get_global_driver()
    _d.clicking(
        ".ant-modal:has(table) .ant-modal-title button", "add new phiếu sàng lọc"
    )


@_trace
def add_all_phieusanglocdinhduong(admission_date: dt.date):
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

    if open_dialog():
        next_date = get_last_date() + dt.timedelta(days=7)
        if next_date <= today:
            _lgr.info(f"add new phieu sang loc for {next_date}")
            add_new()
        else:
            close_dialog()
            return
    else:
        next_date = admission_date

    save_new_phieusangloc(next_date, cannang, chieucao, build_machedo(age_in_month))
    next_date = next_date + dt.timedelta(days=7)

    while next_date <= today:
        _lgr.info(f"add new phieu sang loc for {next_date}")
        open_dialog()
        add_new()
        save_new_phieusangloc(
            next_date,
            cannang,
            chieucao,
            build_machedo(age_in_month),
        )
        next_date = next_date + dt.timedelta(days=7)
