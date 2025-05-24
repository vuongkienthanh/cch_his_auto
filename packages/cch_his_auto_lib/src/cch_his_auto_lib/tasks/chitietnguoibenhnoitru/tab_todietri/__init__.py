import logging
import datetime as dt

from selenium.webdriver.remote.webelement import WebElement

from cch_his_auto_lib.driver import get_global_driver
from cch_his_auto_lib.helper import EndOfLoop, tracing
from .. import _lgr, ACTIVE_PANE

TAB_NUMBER = 3

_lgr = logging.getLogger("tab_todieutri")
_trace = tracing(_lgr)


def show_only_khoalamviec():
    _d = get_global_driver()
    _d.clicking2(f"{ACTIVE_PANE} h1 svg:last-child")
    _d.clicking2(".ant-popover .ant-radio-group label:last-child input")
    _d.clicking2(".ant-popover .ant-radio-group label:first-child input")
    _d.clicking2(f"{ACTIVE_PANE} h1 svg:last-child")


def show_all_khoa():
    _d = get_global_driver()
    _d.clicking2(f"{ACTIVE_PANE} h1 svg:last-child")
    _d.clicking2(".ant-popover .ant-radio-group label:first-child input")
    _d.clicking2(".ant-popover .ant-radio-group label:last-child input")
    _d.clicking2(f"{ACTIVE_PANE} h1 svg:last-child")


def get_all_ngaydieutri() -> list[WebElement]:
    "return only date part"
    _d = get_global_driver()
    return _d.find_all(
        f"{ACTIVE_PANE} .ant-collapse-item>.ant-collapse-header .right>span:first-child"
    )


def get_all_todieutri_at_date(date: dt.date) -> list[WebElement]:
    "return only time part"
    _d = get_global_driver()
    date_str = date.strftime("%d/%m/%Y")
    for i, d in enumerate(get_all_ngaydieutri(), 1):
        if d.text.strip()[:10] == date_str:
            return _d.find_all(
                f"{ACTIVE_PANE} .ant-collapse-item:nth-child({i})>.ant-collapse-content .left"
            )
    else:
        raise EndOfLoop(f"can't find todieutri at date= {date}")


@_trace
def open_nearest_todieutri_to_datetime(_dt: dt.datetime):
    _d = get_global_driver()

    def timeval(time: dt.time) -> int:
        return time.hour * 24 + time.minute * 60

    date = _dt.date()
    time = timeval(_dt.time())

    min(
        get_all_todieutri_at_date(date),
        key=lambda ele: abs(
            time - timeval(dt.datetime.strptime(ele.text.strip(), "%H:%M:%S").time())
        ),
    ).click()
    _d.waiting(f"{ACTIVE_PANE} .ant-collapse-item .actived")
    _d.clicking2(f"{ACTIVE_PANE} .ant-collapse-item .actived .right svg:last-child")
    _d.wait_closing(f"{ACTIVE_PANE} .ant-collapse-item .actived")
