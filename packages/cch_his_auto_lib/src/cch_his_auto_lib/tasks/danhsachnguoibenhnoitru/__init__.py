import logging
import time
import datetime as dt

from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

from cch_his_auto_lib.driver import get_global_driver
from cch_his_auto_lib.helper import tracing
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru import wait_patient_page_loaded

URL = "http://emr.ndtp.org/quan-ly-noi-tru/danh-sach-nguoi-benh-noi-tru"

_lgr = logging.getLogger().getChild("danhsachnguoibenhnoitru")
_trace = tracing(_lgr)


def get_khoalamviec() -> str:
    _d = get_global_driver()
    return _d.waiting(".khoaLamViec div span", "khoa lam viec").text.strip()


@_trace
def filter_trangthainguoibenh(indexes: list[int]):
    """
    Open *Trạng thái người bệnh*.
    Uncheck all checkboxes, then check those in `indexes`.
    `indexes` is 1-indexed.
    Then close it
    """
    _d = get_global_driver()
    _lgr.debug(f"filter_trangthainguoibenh indexes={indexes}")
    _d.clicking(
        ".base-search_component .ant-col:nth-child(7) button",
        " open menu trạng thái người bệnh",
    )
    _d.waiting(".ant-popover label", "danh sách trạng thái người bệnh")
    _lgr.debug("uncheck all boxes in trạng thái người bệnh")
    for ele in _d.find_all(".ant-checkbox-group .ant-checkbox-checked"):
        ele.click()

    _lgr.debug("check boxes based on indexes")
    for i in indexes:
        _d.clicking(
            f".ant-checkbox-group label:nth-child({i}) .ant-checkbox",
            _d.find(f".ant-popover label:nth-child({i})").text,
        )
    _d.clicking(
        ".base-search_component .ant-col:nth-child(7) button",
        "close menu trạng thái người bệnh",
    )
    _d.wait_closing(".ant-popover:has(label:nth-child(10))")


@_trace
def open_filter_boloc():
    "Open filter *Bộ lọc* for subsequent tasks"
    _d = get_global_driver()
    _d.clicking(".base-search_component .ant-col:nth-child(1) button", "Bộ lọc button")
    _d.waiting(".ant-popover .content-popover +div button", "Tìm button")


@_trace
def close_filter_boloc():
    "Close filter *Bộ lọc* after `open_filter_boloc` and finish all tasks inside"
    _d = get_global_driver()
    _d.clicking(".ant-popover .content-popover +div button", "Tìm button")
    _d.wait_closing(".ant-popover .content-popover +div button")


@_trace
def filter_boloc_thoigiannhapvien(start: dt.date, end: dt.date):
    "After `open_filter_boloc`, input admission `start` date and `end` date info"
    _d = get_global_driver()
    _lgr.debug(f"start_date={start}")
    _lgr.debug(f"end_date={end}")
    fmt = "%Y-%m-%d"
    start_d = start.strftime(fmt)
    end_d = end.strftime(fmt)
    _lgr.debug("+++++ typing dates")
    ActionChains(_d).send_keys_to_element(
        _d.find(".date-1 .ant-picker-input input"), start_d
    ).pause(1).send_keys_to_element(
        _d.find(".date-1 .ant-picker-input:nth-child(3) input"), end_d
    ).send_keys(Keys.ENTER).perform()


def filter_patient(ma_hs: int):
    "Filter patient based on `ma_hs`"
    _d = get_global_driver()
    _lgr.debug(f"filter_patient ma_hs={ma_hs}")
    ele = _d.clear_input(".base-search_component .ant-col:nth-child(2) input")
    _lgr.debug("+++++ typing ma_hs to search entry")
    ele.send_keys(str(ma_hs))
    ele.send_keys(Keys.ENTER)
    time.sleep(2)
    _d.waiting_to_be(
        ".ant-table-body tbody tr:nth-child(2) td:nth-child(8)",
        str(ma_hs),
        "first row patient id",
    )


@_trace
def goto_patient(ma_hs: int):
    "Filter patient based on `ma_hs`, then open that patient"
    _d = get_global_driver()
    _lgr.info(f"goto patient ma_hs={ma_hs}")
    filter_patient(ma_hs)
    _d.clicking(
        ".ant-table-body tbody tr:nth-child(2) td:nth-child(30)",
        "first row",
    )
    wait_patient_page_loaded(ma_hs)
