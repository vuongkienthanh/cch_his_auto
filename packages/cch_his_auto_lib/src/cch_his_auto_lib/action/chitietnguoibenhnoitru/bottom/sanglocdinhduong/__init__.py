import datetime as dt

from selenium.common import NoSuchElementException

from cch_his_auto_lib.action import top_patient_info
from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.action.chitietnguoibenhnoitru.bottom import _lgr, _trace


from .helper import machedo, calculate_age_in_months
from . import phieusangloc

URL = "http://emr.ndtp.org/quan-ly-dinh-duong/phieu-sang-loc/"
DIALOG_CSS = ".ant-modal:has(.rightTitle):has(table)"


def open_dialog(d: Driver) -> bool:
    "Open *Sàng lọc dinh dưỡng* dialog"
    current_url = d.current_url
    try:
        d.clicking(".footer-btn .right button:nth-child(1)")
        d.waiting(DIALOG_CSS, "Sàng lọc dinh dưỡng dialog")
        return True
    except NoSuchElementException:
        _lgr.warning("can't open sanglocdinhduong dialog")
        d.goto(current_url)
        top_patient_info.wait_loaded(d)
        return False


def close_dialog(d: Driver):
    "Close *Sàng lọc dinh dưỡng* dialog"
    d.clicking(f"{DIALOG_CSS} button.ant-modal-close")
    d.wait_closing(DIALOG_CSS)


def open_phieusangloc(d: Driver, i: int):
    "Open phieusangloc at `i` index, start at 2"
    d.clicking2(f"{DIALOG_CSS} tbody tr:nth-child({i}) td:last-child svg")


@_trace
def get_chieucao_cannang_from_first_phieusangloc(d: Driver) -> tuple[str, str] | None:
    if not open_dialog(d):
        return None

    open_phieusangloc(d, 2)
    top_patient_info.wait_loaded(d)
    cc = phieusangloc.get_chieucao(d)
    cn = phieusangloc.get_cannang(d)
    phieusangloc.back(d)
    if (cc is None) or (cn is None):
        return None
    return (cc, cn)


def get_last_date(d: Driver) -> dt.date:
    "Get last date in *Sàng lọc dinh dưỡng* dialog"
    max_rank = 0
    max_i = 0
    for i in range(2, 12):
        try:
            rank = d.find(
                f"{DIALOG_CSS} tbody tr:nth-child({i}) td:nth-child(3)"
            ).text.strip()
            if (r := int(rank)) > max_rank:
                max_rank = r
                max_i = i
        except:
            break
    date = dt.datetime.strptime(
        d.find(f"tbody tr:nth-child({max_i}) td:nth-child(2)").text.strip(),
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
def add_all_phieusanglocdinhduong(d: Driver):
    "Complete all *Phiếu sàng lọc* from admission_date up til today"
    get_chieucao_cannang = get_chieucao_cannang_from_first_phieusangloc(d)
    if get_chieucao_cannang:
        chieucao, cannang = get_chieucao_cannang
    else:
        _lgr.warning("can't add all phieusanglocidinhduong")
        return

    today = dt.date.today()
    chedo = machedo(
        calculate_age_in_months(
            dt.datetime.strptime(
                top_patient_info.get_patient_info(d)["birthdate"], "%d/%m/%Y"
            )
        )
    )
    open_dialog(d)
    next_date = get_last_date(d) + dt.timedelta(days=7)
    close_dialog(d)

    while next_date <= today:
        _lgr.info(f"add new phieu sang loc for {next_date}")
        open_dialog(d)
        add_new(d)
        phieusangloc.save_new_phieusangloc(d, next_date, cannang, chieucao, chedo)
        next_date = next_date + dt.timedelta(days=7)
