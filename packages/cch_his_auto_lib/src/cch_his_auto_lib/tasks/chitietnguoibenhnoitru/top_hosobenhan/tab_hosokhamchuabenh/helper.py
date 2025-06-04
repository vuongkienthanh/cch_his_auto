from enum import StrEnum
import datetime as dt
import time
from typing import Callable
from functools import partial

from selenium.webdriver import Keys
from selenium.common import NoSuchElementException, StaleElementReferenceException

from cch_his_auto_lib.driver import get_global_driver
from .. import ACTIVE_PANE
from . import _lgr


RIGHT_PANEL = f"{ACTIVE_PANE} .right-content"


def do_nothing(*_):
    _lgr.warning("do nothing")


def sign_current(i: int):
    _d = get_global_driver()
    _d.clicking(f"{RIGHT_PANEL} tr:nth-child({i})")
    _d.clicking(
        f"{RIGHT_PANEL} .__action button:nth-child(2)", "clicking Ký tên BS dieu tri"
    )


def sign_current2(i: int):
    _d = get_global_driver()
    _d.clicking(f"{RIGHT_PANEL} tr:nth-child({i})")
    _d.clicking(
        f"{RIGHT_PANEL} .__action button:nth-child(3)", "clicking Ký tên BS truong khoa"
    )


def sign_current_both(i: int):
    sign_current(i)
    sign_current2(i)


def goto_row_then_tabdo(i: int, sign_fn: Callable):
    _d = get_global_driver()
    _d.clicking(f"{RIGHT_PANEL} tr:nth-child({i})")
    tab0 = _d.current_window_handle
    datakey = _d.find(f"{RIGHT_PANEL} tr:nth-child({i})").get_attribute("data-row-key")
    _lgr.debug(f"data row key = {datakey}")
    _d.clicking(f"{RIGHT_PANEL} tr:nth-child({i})", f"row {i - 1}")
    time.sleep(2)
    _d.clicking(f"a[data-key='{datakey}'] button", f"edit button {i - 1}")
    _d.goto_newtab_do_smth_then_goback(tab0, sign_fn)


class Status(StrEnum):
    "Possible status for each document"

    CHUAKY = "Chưa ký"
    DANGKY = "Đang ký"
    HOANTHANH = "Hoàn thành"


def filter(name: str) -> bool:
    "Filter document based on `name`"
    _lgr.debug(f"name={name}")
    _d = get_global_driver()
    ele = _d.clear_input(f"{RIGHT_PANEL} input")
    _lgr.debug("+++++ typing name")
    ele.send_keys(name)
    ele.send_keys(Keys.ENTER)
    for _ in range(60):  # 120 is too long
        time.sleep(1)
        try:
            ele = _d.find(f"{RIGHT_PANEL} tr:nth-child(2) td:nth-child(2) div")
            if ele.text.strip().startswith(name):
                _lgr.info(f"-> found {name}")
                return True
        except NoSuchElementException:
            ...
    else:
        _lgr.warning(f"-> filtered {name} with no result")
        return False


def is_row_status(idx: int, status: Status) -> bool:
    "Check if row at `idx` is `status`, first row is idx=2"
    _d = get_global_driver()
    try:
        _lgr.debug(f"checking status = {status}")
        return (
            _d.waiting(
                f"{RIGHT_PANEL} tr:nth-child({idx}) td:nth-child(3)",
                f"row {idx} status",
            ).text.strip()
            == status
        )
    except StaleElementReferenceException:
        return is_row_status(idx, status)


def is_row_expandable(idx: int) -> bool:
    "Check if row at `idx` is expandable, first row is idx=2"
    _d = get_global_driver()
    name = _d.waiting(
        f"{RIGHT_PANEL} tr:nth-child({idx}) td:nth-child(2)", f"row {idx}"
    ).text
    _lgr.debug(f"checking {name}: expandable")
    for _ in range(5):
        time.sleep(1)
        try:
            ele = _d.find(f"{RIGHT_PANEL} tr:nth-child({idx}) td:nth-child(1) button")
            class_list = ele.get_attribute("class")
            assert class_list is not None
            return "ant-table-row-expand-icon-collapsed" in class_list
        except (NoSuchElementException, StaleElementReferenceException):
            continue
    else:
        return False


def expand_row(idx: int):
    "Expand row at `idx`, first row is idx=2"
    _d = get_global_driver()
    name = _d.waiting(
        f"{RIGHT_PANEL} tr:nth-child({idx}) td:nth-child(2)", f"row {idx}"
    ).text
    _lgr.info(f"expanding {name}")
    _d.clicking(f"{RIGHT_PANEL} tr:nth-child({idx}) td:nth-child(1) button")


def filter_check_expand_sign(
    name: str,
    chuaky_fn: Callable[[int], None] = do_nothing,
    dangky_fn: Callable[[int], None] = do_nothing,
    date: dt.date | None = None,
):
    """
    filter `name`, expand it if possible, then call `fn` respectively bases on status
    if `date` provided, only sign those with this date
    """
    _d = get_global_driver()

    def check_and_sign(i: int):
        name = _d.waiting(f"{RIGHT_PANEL} tr:nth-child({i}) td:nth-child(2)").text
        _lgr.debug(f"checking {name}")
        if is_row_status(i, Status.CHUAKY):
            _lgr.info(f"row condition: not met: {name} -> {Status.CHUAKY}")
            chuaky_fn(i)
            time.sleep(5)
        elif is_row_status(i, Status.DANGKY):
            _lgr.info(f"row condition: not met: {name} -> {Status.DANGKY}")
            dangky_fn(i)
            time.sleep(5)
        else:
            _lgr.info("row condition: OK")

    def check_and_sign_date(i: int, date: dt.date):
        name = _d.waiting(f"{RIGHT_PANEL} tr:nth-child({i}) td:nth-child(2)").text
        _lgr.debug(f"checking {name} with date={date}")
        if name.lstrip().startswith(date.strftime("%d/%m/%Y")):
            if is_row_status(i, Status.CHUAKY):
                _lgr.info(f"row condition: not met: {name} -> {Status.CHUAKY}")
                chuaky_fn(i)
                time.sleep(5)
            elif is_row_status(i, Status.DANGKY):
                _lgr.info(f"row condition: not met: {name} -> {Status.DANGKY}")
                dangky_fn(i)
                time.sleep(5)
            else:
                _lgr.info("row condition: OK")
        else:
            _lgr.debug("-> skip date")

    if filter(name) and (
        _d.waiting(f"{RIGHT_PANEL} tr:nth-child(2) td:nth-child(3)").text.strip()
        != Status.HOANTHANH
    ):
        if is_row_expandable(2):
            if date:
                check_and_sign2 = partial(check_and_sign_date, date=date)
            else:
                check_and_sign2 = check_and_sign

            expand_row(2)
            for i in range(
                3, len(_d.find_all(f"{RIGHT_PANEL} .ant-table-row-level-1")) + 3
            ):
                check_and_sign2(i)
        else:
            check_and_sign(2)
