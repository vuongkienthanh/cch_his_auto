import logging
import time
import datetime as dt
from contextlib import contextmanager

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tracing import tracing
from cch_his_auto_lib.action import top_patient_info

URL = "http://emr.ndtp.org/quan-ly-noi-tru/danh-sach-nguoi-benh-noi-tru"

_lgr = logging.getLogger("danhsachnguoibenhnoitru")
_trace = tracing(_lgr)


def wait_loaded(d: Driver):
    try:
        WebDriverWait(d, 120).until(
            lambda _: len(d.find_all(".main__container tr.ant-table-row")) >= 1
        )
    except TimeoutException:
        d.refresh()
        WebDriverWait(d, 120).until(
            lambda _: len(d.find_all(".main__container tr.ant-table-row")) >= 1
        )
    finally:
        time.sleep(5)


def load(d: Driver):
    d.goto(URL)
    wait_loaded(d)
    huytimkiem(d)


def get_khoalamviec(d: Driver) -> str:
    return d.waiting(".khoaLamViec div span", "khoa lam viec").text.strip()


def huytimkiem(d: Driver):
    d.clicking(
        "#base-search_component > div > div:nth-child(2) button:first-child",
        "Hủy tìm kiếm button",
    )
    time.sleep(5)  # no change on UI


TRANGTHAINGUOIBENH_POPOVER = ".ant-popover:has(.check-all)"


@contextmanager
def open_trangthainguoibenh(d: Driver):
    "Open and close *Trạng thái người bệnh* as a context manager"
    d.clicking(
        "#base-search_component .ant-col:nth-child(7) button",
        " open menu trạng thái người bệnh",
    )
    d.waiting(f"{TRANGTHAINGUOIBENH_POPOVER} .check-all")
    try:
        yield
    finally:
        d.clicking(
            "#base-search_component .ant-col:nth-child(7) button",
            "close menu trạng thái người bệnh",
        )
        d.wait_closing(TRANGTHAINGUOIBENH_POPOVER)


@_trace
def filter_trangthainguoibenh(d: Driver, indexes: list[int]):
    """
    Open *Trạng thái người bệnh*
    Uncheck all checkboxes, then check those in `indexes`.
    `indexes` is 1-indexed.
    """
    _lgr.debug(f"filter_trangthainguoibenh indexes={indexes}")
    with open_trangthainguoibenh(d):
        _lgr.debug("uncheck all boxes in trạng thái người bệnh")
        ele = d.find(f"{TRANGTHAINGUOIBENH_POPOVER} .check-all .ant-checkbox input")
        if ele.is_selected():
            ele.click()
        else:
            ele.click()
            ele.click()

        for i in indexes:
            d.clicking(
                f"{TRANGTHAINGUOIBENH_POPOVER} .ant-checkbox-group label:nth-child({i}) .ant-checkbox input",
                d.find(f".ant-popover label:nth-child({i})").text,
            )


@_trace
def filter_trangthainguoibenh_check_all(d: Driver):
    """
    Open *Trạng thái người bệnh*.
    Check all checkboxes
    """
    with open_trangthainguoibenh(d):
        ele = d.find(f"{TRANGTHAINGUOIBENH_POPOVER} .check-all .ant-checkbox input")
        if not ele.is_selected():
            ele.click()


BOLOC_POPOVER = ".ant-popover:has(form +div button)"


@contextmanager
def open_boloc(d: Driver):
    "Open and close *Bộ lọc* as a context manager"
    d.clicking("#base-search_component .ant-col:nth-child(1) button", "Bộ lọc button")
    d.waiting(BOLOC_POPOVER)
    try:
        yield
    finally:
        d.clicking(f"{BOLOC_POPOVER} form +div button", "Tìm button")
        d.wait_closing(BOLOC_POPOVER)


@_trace
def filter_boloc(
    d: Driver,
    vaokhoa: tuple[dt.date, dt.date] | None = None,
    nhapvien: tuple[dt.date, dt.date] | None = None,
    ravien: tuple[dt.date, dt.date] | None = None,
):
    """
    Open *Bộ lọc*
    input date info
    """
    if not any([vaokhoa, nhapvien, ravien]):
        return
    fmt = "%Y-%m-%d"

    with open_boloc(d):
        for loc, date in zip([8, 11, 14], [vaokhoa, nhapvien, ravien]):
            if date is None:
                continue
            start_d = date[0].strftime(fmt)
            end_d = date[1].strftime(fmt)
            d.clear_input(
                f"{BOLOC_POPOVER} form .ant-form-item.date-1:nth-child({loc}) .ant-picker-input:nth-child(1) input"
            ).send_keys(start_d)
            d.clear_input(
                f"{BOLOC_POPOVER} form .ant-form-item.date-1:nth-child({loc}) .ant-picker-input:nth-child(3) input"
            ).send_keys(end_d)


MAIN_TABLE = "#base-search_component +div .ant-table table tbody"


def filter_patient(d: Driver, ma_hs: int):
    "Filter patient based on `ma_hs`"
    _lgr.debug(f"filter_patient ma_hs={ma_hs}")
    ele = d.clear_input(".base-search_component .ant-col:nth-child(2) input")
    ele.send_keys(str(ma_hs))
    ele.send_keys(Keys.ENTER)
    d.wait_closing(f"{MAIN_TABLE} .ant-table-row:nth-child(3)")


def goto_patient(d: Driver, ma_hs: int):
    "Filter patient based on `ma_hs`, then open that patient"
    filter_patient(d, ma_hs)
    open_patient(d, 2)


@_trace
def open_patient(d: Driver, i: int):
    d.clicking2(f"{MAIN_TABLE} tr.ant-table-row:nth-child({i}) td:last-child svg")
    top_patient_info.wait_loaded(d)


def has_next_page(d: Driver) -> bool:
    try:
        d.waiting(".ant-pagination-next:not(.ant-pagination-disabled)")
        return True
    except NoSuchElementException:
        return False


def next_page(d: Driver):
    current_page = d.waiting(
        ".ant-pagination.patient-paging li.ant-pagination-item-active"
    ).get_attribute("title")
    assert current_page is not None
    next_page = int(current_page) + 1
    d.clicking(".ant-pagination-next:not(.ant-pagination-disabled) button")
    d.waiting(
        f".ant-pagination.patient-paging li.ant-pagination-item-active[title='{next_page}']"
    )
    time.sleep(5)
