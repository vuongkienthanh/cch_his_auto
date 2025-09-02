import logging
import datetime as dt
from functools import partial
from typing import Callable

from selenium.webdriver import Keys

from cch_his_auto_lib.driver import Driver, DriverFn
from cch_his_auto_lib.action import editor

URL = "http://emr.ndtp.org/hoi-chan"


_lgr = logging.getLogger("hoichan")


def wait_loaded(d: Driver):
    d.waiting(".main__container")


def load(d: Driver):
    d.goto(URL)
    wait_loaded(d)


def set_dept(d: Driver, dept: str):
    CSS = ".ant-popover:has(form + div button)"
    d.clicking("#base-search_component .ant-col .ant-col:first-child button")
    try:
        d.clicking2(
            ".ant-popover:has(form + div button) form .ant-form-item:first-child .ant-select"
        )
        ele = d.clear_input(
            ".ant-popover:has(form + div button) form .ant-form-item:first-child input"
        )
        ele.send_keys(dept)
        ele.send_keys(Keys.ENTER)
        d.clicking2(
            ".ant-popover:has(form + div button) form .ant-form-item:nth-child(2) .ant-select"
        )
        ele = d.clear_input(
            ".ant-popover:has(form + div button) form .ant-form-item:nth-child(2) input"
        )
        ele.send_keys(dept)
        ele.send_keys(Keys.ENTER)
    finally:
        d.clicking(f"{CSS} button")
        d.wait_disappearing(CSS)


def set_date(d: Driver, date: dt.date):
    fmt = "%d/%m/%Y %H:%M:%S"
    s = dt.datetime(date.year, date.month, date.day, 0, 0, 0).strftime(fmt)
    e = dt.datetime(date.year, date.month, date.day, 23, 59, 59).strftime(fmt)
    d.clear_input(
        "#base-search_component .ant-col .ant-col:nth-child(3) .ant-picker-input:first-child input"
    ).send_keys(s)
    d.clear_input(
        "#base-search_component .ant-col .ant-col:nth-child(3) .ant-picker-input:nth-child(3) input"
    ).send_keys(e)


MAIN_TABLE = "#base-search_component +div .ant-table table tbody"


def iterate_all_and_do(d: Driver, open_fn: Callable[[Driver, int], None], f: DriverFn):
    def do(d, i):
        open_fn(d, i)
        f(d)

    for i in range(2, len(d.find_all(f"{MAIN_TABLE} tr.ant-table-row")) + 2):
        d.duplicate_tab_do(partial(do, i=i))


def open_BBHC_editor(d: Driver, i: int):
    d.clicking2(f"{MAIN_TABLE} tr.ant-table-row:nth-child({i}) td:last-child svg:nth-child(3)")
    d.clicking(f".ant-dropdown li:first-child a")
    editor.wait_loaded(d)
