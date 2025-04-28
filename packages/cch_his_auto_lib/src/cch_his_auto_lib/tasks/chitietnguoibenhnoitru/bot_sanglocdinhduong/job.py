import datetime as dt

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.helper import tracing
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru import (
    top_chitietthongtin,
)

from . import (
    _logger,
    open_dialog,
    close_dialog,
    get_last_date,
    save,
    set_cannang,
    add_new,
    set_date,
    set_chieucao,
)

_trace = tracing(_logger)


@_trace
def save_new_phieusangloc(driver: Driver, date: dt.date, cannang: str, chieucao: str):
    "Complete this *Phiếu sàng lọc* then go back to *Chi tiết bệnh nhân nội trú*"
    _logger.info(f"new phieusangloc: date= {date}")
    set_date(driver, date)
    set_cannang(driver, cannang)
    set_chieucao(driver, chieucao)
    save(driver)


@_trace
def add_all_phieusanglocdinhduong(driver: Driver, admission_date: dt.date):
    "Complete all *Phiếu sàng lọc* from admission_date up til today"
    with top_chitietthongtin.session(driver):
        cannang = top_chitietthongtin.get_cannang(driver)
        if not cannang:
            _logger.warning("cannang is empty -> skip Sàng lọc dinh dưỡng")
            return
        chieucao = top_chitietthongtin.get_chieucao(driver)
        if not chieucao:
            _logger.warning("chieucao is empty -> skip Sàng lọc dinh dưỡng")
            return

    today = dt.date.today()

    if open_dialog(driver):
        next_date = get_last_date(driver) + dt.timedelta(days=7)
        if next_date <= today:
            add_new(driver)
        else:
            close_dialog(driver)
            return
    else:
        next_date = admission_date

    save_new_phieusangloc(driver, next_date, cannang, chieucao)
    next_date = next_date + dt.timedelta(days=7)

    while next_date <= today:
        open_dialog(driver)
        add_new(driver)
        save_new_phieusangloc(driver, next_date, cannang, chieucao)
        next_date = next_date + dt.timedelta(days=7)
