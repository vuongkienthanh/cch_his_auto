import logging
import datetime as dt

from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tracing import tracing
from cch_his_auto_lib.action.chitietnguoibenhnoitru.tabs import (
    change_tab,
    thongtinchung,
    todieutri,
)
from cch_his_auto_lib.action import todieutria
from .. import ACTIVE_PANE


TAB_NUMBER = 6

_lgr = logging.getLogger("tab_soket15ngay")
_trace = tracing(_lgr)

from .phieusoket import save_new_phieusoket


def get_last_date(d: Driver) -> dt.date | None:
    "Assume first row is the latest *sơ kết 15 ngày* , get that end_date"
    try:
        ele = d.waiting(
            f"{ACTIVE_PANE} tbody .ant-table-row-level-0:nth-child(2) td:nth-child(9)"
        ).text.strip()
        if ele == "":
            return None
        else:
            _lgr.info(f"last_date= {ele}")
            return dt.datetime.strptime(ele, "%d/%m/%Y").date()
    except NoSuchElementException:
        _lgr.warning("-> can't find last_date")
        return None


def add_new(d: Driver):
    "Add new *Phiếu sơ kết 15 ngày*"
    d.clicking(f"{ACTIVE_PANE} button")


###
# NOTE:
# selenium can't handle print dialog when saved new phieu so ket
###
# @_trace
# def add_all_phieusoket15ngay(driver: Driver, admission_date: dt.date):
#     "Complete all *Phiếu sơ kết* from admission_date up til today"
#
#     last_date = get_last_date(driver)
#     if last_date is None:
#         start_date = admission_date
#         end_date = start_date + dt.timedelta(days=7)
#     else:
#         start_date = last_date + dt.timedelta(days=1)
#         end_date = start_date + dt.timedelta(days=7)
#     if end_date > dt.date.today():
#         return
#
#     change_tab(driver, tab_todietri.TAB_NUMBER)
#     tab_todietri.show_all_khoa(driver)
#     tab_todietri.open_nearest_todieutri_to_datetime(
#         driver, dt.datetime(end_date.year, end_date.month, end_date.day, 7, 0, 0)
#     )
#
#     change_tab(driver, TAB_NUMBER)
