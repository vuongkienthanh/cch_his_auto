from enum import Enum
import datetime as dt
import time
from typing import Callable

from selenium.webdriver import Keys
from selenium.common import NoSuchElementException, StaleElementReferenceException

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.action import editor
from .. import ACTIVE_PANE
from . import _lgr


RIGHT_PANEL = f"{ACTIVE_PANE} .right-content"

SIGN_AT_ROW_FN = Callable[[Driver, int], None]


def do_nothing(_d: Driver, *_):
    _lgr.warning("do nothing")


def sign_current(d: Driver, i: int):
    d.clicking(f"{RIGHT_PANEL} tr:nth-child({i})")
    d.clicking(
        f"{RIGHT_PANEL} .__action button:nth-child(2)", "clicking Ký tên BS dieu tri"
    )


def sign_current2(d: Driver, i: int):
    d.clicking(f"{RIGHT_PANEL} tr:nth-child({i})")
    d.clicking(
        f"{RIGHT_PANEL} .__action button:nth-child(3)", "clicking Ký tên BS truong khoa"
    )


def sign_current_both(d: Driver, i: int):
    sign_current(d, i)
    sign_current2(d, i)


def goto_row_and_click_edit(d: Driver, i: int):
    d.clicking(f"{RIGHT_PANEL} tr:nth-child({i})", f"row {i - 1}")
    datakey = d.find(f"{RIGHT_PANEL} tr:nth-child({i})").get_attribute("data-row-key")
    _lgr.debug(f"data row key = {datakey}")
    time.sleep(2)
    d.clicking(f"a[data-key='{datakey}'] button", f"edit button {i - 1}")
    editor.wait_loaded(d)


def filter_check_expand_sign(
    d: Driver,
    name: str,
    chuaky_fn: SIGN_AT_ROW_FN = do_nothing,
    dangky_fn: SIGN_AT_ROW_FN = do_nothing,
    date: dt.date | None = None,
):
    """
    filter `name`, expand it if possible, then call `fn` respectively bases on status
    if `date` provided, only sign those with this date
    """

    class Status(Enum):
        "Possible statuses for each document"

        CHUAKY = "Chưa ký"
        DANGKY = "Đang ký"
        HOANTHANH = "Hoàn thành"

    def is_row_status(d: Driver, idx: int, status: Status) -> bool:
        "Check if row at `idx` is `status`, first row is idx=2"
        try:
            _lgr.debug(f"checking status = {status.value}")
            return (
                d.waiting(
                    f"{RIGHT_PANEL} tr:nth-child({idx}) td:nth-child(3)",
                    f"row {idx} status",
                ).text.strip()
                == status.value
            )
        except StaleElementReferenceException:
            return is_row_status(d, idx, status)

    def filter(d: Driver, name: str) -> bool:
        "Filter document based on `name`"
        _lgr.debug(f"filter hosobenhan name={name}")
        ele = d.clear_input(f"{RIGHT_PANEL} input:nth-child(3)")
        ele.send_keys(name)
        ele.send_keys(Keys.ENTER)
        for _ in range(60):  # 120 is too long
            time.sleep(1)
            try:
                ele = d.find(f"{RIGHT_PANEL} tr:nth-child(2) td:nth-child(2) div")
                if ele.text.strip().startswith(name):
                    _lgr.info(f"-> filter hosobenhan: found {name}")
                    return True
            except NoSuchElementException:
                ...
        else:
            _lgr.warning(f"-> filter hosobenhan: can't find {name}")
            return False

    def is_row_expandable(d: Driver, idx: int) -> bool:
        "Check if row at `idx` is expandable, first row is idx=2"
        name = d.waiting(
            f"{RIGHT_PANEL} tr:nth-child({idx}) td:nth-child(2)", f"row {idx}"
        ).text
        _lgr.debug(f"checking {name}: expandable")
        for _ in range(5):
            time.sleep(1)
            try:
                ele = d.find(
                    f"{RIGHT_PANEL} tr:nth-child({idx}) td:nth-child(1) button"
                )
                class_list = ele.get_attribute("class")
                assert class_list is not None
                return "ant-table-row-expand-icon-collapsed" in class_list
            except (NoSuchElementException, StaleElementReferenceException):
                continue
        else:
            return False

    def expand_row(d: Driver, idx: int):
        "Expand row at `idx`, first row is idx=2"
        name = d.waiting(
            f"{RIGHT_PANEL} tr:nth-child({idx}) td:nth-child(2)", f"row {idx}"
        ).text
        _lgr.debug(f"expanding {name}")
        d.clicking(
            f"{RIGHT_PANEL} tr:nth-child({idx}) td:nth-child(1) button.ant-table-row-expand-icon-collapsed"
        )

    def check_and_sign(
        d: Driver, i: int, chuaky_fn: SIGN_AT_ROW_FN, dangky_fn: SIGN_AT_ROW_FN
    ):
        name = d.waiting(f"{RIGHT_PANEL} tr:nth-child({i}) td:nth-child(2)").text
        _lgr.debug(f"checking {name}")
        if is_row_status(d, i, Status.CHUAKY):
            _lgr.info(f"row condition not met -> {Status.CHUAKY.value}")
            chuaky_fn(d, i)
            time.sleep(3)
        elif is_row_status(d, i, Status.DANGKY):
            _lgr.info(f"row condition not met -> {Status.DANGKY.value}")
            dangky_fn(d, i)
            time.sleep(3)
        else:
            _lgr.info("row condition: OK")

    def expanded_check_and_sign(
        d: Driver,
        i: int,
        chuaky_fn: SIGN_AT_ROW_FN,
        dangky_fn: SIGN_AT_ROW_FN,
        date: dt.date | None = None,
    ):
        name = d.waiting(f"{RIGHT_PANEL} tr:nth-child({i}) td:nth-child(2)").text
        try:
            row_date = dt.datetime.strptime(name.lstrip()[:10], "%d/%m/%Y").date()
            _lgr.info(f"row date = {row_date}")
        except ValueError:
            _lgr.warning("can't parse date. Maybe this line has no date info.")
        else:
            if date is None:
                if row_date > dt.date.today():
                    _lgr.info("-> skipped")
                    return
            else:
                if row_date != date:
                    _lgr.info("-> skipped")
                    return

        if is_row_status(d, i, Status.CHUAKY):
            _lgr.info(f"row condition not met -> {Status.CHUAKY.value}")
            chuaky_fn(d, i)
            time.sleep(3)
        elif is_row_status(d, i, Status.DANGKY):
            _lgr.info(f"row condition not met -> {Status.DANGKY.value}")
            dangky_fn(d, i)
            time.sleep(3)
        else:
            _lgr.info("row condition: OK")

    if filter(d, name) and not is_row_status(d, 2, Status.HOANTHANH):
        if is_row_expandable(d, 2):
            expand_row(d, 2)
            for i in range(
                3, len(d.find_all(f"{RIGHT_PANEL} .ant-table-row-level-1")) + 3
            ):
                expanded_check_and_sign(d, i, chuaky_fn, dangky_fn, date)
        else:
            check_and_sign(d, 2, chuaky_fn, dangky_fn)
