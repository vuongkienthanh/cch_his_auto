import logging
import time
import datetime as dt

from selenium.common import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tracing import tracing
from cch_his_auto_lib.action.chitietnguoibenhnoitru import wait_patient_page_loaded

URL = "http://emr.ndtp.org/quan-ly-noi-tru/danh-sach-nguoi-benh-noi-tru"

_lgr = logging.getLogger().getChild("danhsachnguoibenhnoitru")
_trace = tracing(_lgr)


def get_khoalamviec(d: Driver) -> str:
    return d.waiting(".khoaLamViec div span", "khoa lam viec").text.strip()


def huytimkiem(d: Driver):
    d.clicking(
        ".base-search_component > div > div:nth-child(2) button:first-child",
        "Hủy tìm kiếm button",
    )
    time.sleep(5)  # no change on UI


TRANGTHAINGUOIBENH_POPOVER = ".ant-popover:has(.check-all)"


@_trace
def filter_trangthainguoibenh(d: Driver, indexes: list[int]):
    """
    Open *Trạng thái người bệnh*.
    Uncheck all checkboxes, then check those in `indexes`.
    `indexes` is 1-indexed.
    Then close it
    """
    _lgr.debug(f"filter_trangthainguoibenh indexes={indexes}")
    d.clicking(
        ".base-search_component .ant-col:nth-child(7) button",
        " open menu trạng thái người bệnh",
    )
    d.waiting(f"{TRANGTHAINGUOIBENH_POPOVER} .check-all")
    try:
        _lgr.debug("uncheck all boxes in trạng thái người bệnh")
        try:
            ele = d.find(
                f"{TRANGTHAINGUOIBENH_POPOVER} .check-all .ant-checkbox-checked"
            )
            ele.click()
        except NoSuchElementException:
            ele = d.find(f"{TRANGTHAINGUOIBENH_POPOVER} .check-all .ant-checkbox")
            ele.click()
            ele.click()

        _lgr.debug("check boxes based on indexes")
        for i in indexes:
            d.clicking(
                f"{TRANGTHAINGUOIBENH_POPOVER} .ant-checkbox-group label:nth-child({i}) .ant-checkbox",
                d.find(f".ant-popover label:nth-child({i})").text,
            )
    finally:
        d.clicking(
            ".base-search_component .ant-col:nth-child(7) button",
            "close menu trạng thái người bệnh",
        )
        d.wait_closing(TRANGTHAINGUOIBENH_POPOVER)


@_trace
def filter_trangthainguoibenh_check_all(d: Driver):
    """
    Open *Trạng thái người bệnh*.
    check all checkboxes
    Then close it
    """
    d.clicking(
        ".base-search_component .ant-col:nth-child(7) button",
        " open menu trạng thái người bệnh",
    )
    d.waiting(".ant-popover label", "danh sách trạng thái người bệnh")
    d.waiting(".check-all .ant-checkbox", "danh sách trạng thái người bệnh")
    if not d.find(".check-all .ant-checkbox input").is_selected():
        d.clicking(".check-all .ant-checkbox", "check all")

    d.clicking(
        ".base-search_component .ant-col:nth-child(7) button",
        "close menu trạng thái người bệnh",
    )
    d.wait_closing(".ant-popover:has(label:nth-child(10))")


@_trace
def open_filter_boloc(d: Driver):
    "Open filter *Bộ lọc* for subsequent tasks"
    d.clicking(".base-search_component .ant-col:nth-child(1) button", "Bộ lọc button")
    d.waiting(".ant-popover .content-popover +div button", "Tìm button")


@_trace
def close_filter_boloc(d: Driver):
    "Close filter *Bộ lọc* after `open_filter_boloc` and finish all tasks inside"
    d.clicking(".ant-popover .content-popover +div button", "Tìm button")
    d.wait_closing(".ant-popover .content-popover +div button")


@_trace
def filter_boloc_thoigiannhapvien(d: Driver, start: dt.date, end: dt.date):
    "After `open_filter_boloc`, input admission `start` date and `end` date info"
    _lgr.debug(f"start_date={start}")
    _lgr.debug(f"end_date={end}")
    fmt = "%Y-%m-%d"
    start_d = start.strftime(fmt)
    end_d = end.strftime(fmt)
    _lgr.debug("+++++ typing dates")
    ActionChains(d).send_keys_to_element(
        d.find(".date-1 .ant-picker-input input"), start_d
    ).pause(1).send_keys_to_element(
        d.find(".date-1 .ant-picker-input:nth-child(3) input"), end_d
    ).send_keys(Keys.ENTER).perform()


def filter_patient(d: Driver, ma_hs: int):
    "Filter patient based on `ma_hs`"
    _lgr.debug(f"filter_patient ma_hs={ma_hs}")
    ele = d.clear_input(".base-search_component .ant-col:nth-child(2) input")
    _lgr.debug("+++++ typing ma_hs to search entry")
    ele.send_keys(str(ma_hs))
    ele.send_keys(Keys.ENTER)
    time.sleep(2)
    d.waiting_to_startswith(
        ".ant-table-body tbody tr:nth-child(2) td:nth-child(8)",
        str(ma_hs),
        "first row patient id",
    )


@_trace
def goto_patient(d: Driver, ma_hs: int):
    "Filter patient based on `ma_hs`, then open that patient"
    _lgr.info(f"goto patient ma_hs={ma_hs}")
    filter_patient(d, ma_hs)
    d.clicking(
        ".ant-table-body tbody tr:nth-child(2) td:nth-child(30)",
        "first row",
    )
    wait_patient_page_loaded(d, ma_hs)
