import logging
import datetime as dt

from selenium.common import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tracing import tracing
from .. import _lgr, ACTIVE_PANE

TAB_NUMBER = 2

_lgr = logging.getLogger("tab_todieutri")
_trace = tracing(_lgr)


def show_only_khoalamviec(d: Driver):
    d.clicking2(f"{ACTIVE_PANE} h1 svg:last-child")
    d.clicking2(".ant-popover .ant-radio-group label:last-child input")
    d.clicking2(".ant-popover .ant-radio-group label:first-child input")
    d.clicking2(f"{ACTIVE_PANE} h1 svg:last-child")


def show_all_khoa(d: Driver):
    d.clicking2(f"{ACTIVE_PANE} h1 svg:last-child")
    d.clicking2(".ant-popover .ant-radio-group label:first-child input")
    d.clicking2(".ant-popover .ant-radio-group label:last-child input")
    d.clicking2(f"{ACTIVE_PANE} h1 svg:last-child")


def get_all_ngaydieutri(d: Driver) -> list[WebElement]:
    "return only date part"
    return d.find_all(
        f"{ACTIVE_PANE} .ant-collapse-item>.ant-collapse-header .right>span:first-child"
    )


def get_all_todieutri_at_date(d: Driver, date: dt.date) -> list[WebElement]:
    "return only time part"
    date_str = date.strftime("%d/%m/%Y")
    for i, ele in enumerate(get_all_ngaydieutri(d), 1):
        if ele.text.strip()[:10] == date_str:
            return d.find_all(
                f"{ACTIVE_PANE} .ant-collapse-item:nth-child({i})>.ant-collapse-content .left"
            )
    else:
        raise NoSuchElementException(f"can't find todieutri at date= {date}")


@_trace
def open_nearest_todieutri_to_datetime(d: Driver, _dt: dt.datetime):
    def timeval(time: dt.time) -> int:
        return time.hour * 24 + time.minute * 60

    date = _dt.date()
    time = timeval(_dt.time())

    min(
        get_all_todieutri_at_date(d, date),
        key=lambda ele: abs(
            time - timeval(dt.datetime.strptime(ele.text.strip(), "%H:%M:%S").time())
        ),
    ).click()
    d.waiting(f"{ACTIVE_PANE} .ant-collapse-item .actived")
    d.clicking2(f"{ACTIVE_PANE} .ant-collapse-item .actived .right svg:last-child")
    d.wait_disappearing(f"{ACTIVE_PANE} .ant-collapse-item .actived")
