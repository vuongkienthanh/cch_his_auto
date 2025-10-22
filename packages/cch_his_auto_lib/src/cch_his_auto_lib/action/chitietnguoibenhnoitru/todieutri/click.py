import datetime as dt


from .. import ACTIVE_PANE
from .get import get_all_todieutri_at_date
from cch_his_auto_lib.driver import Driver


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
    d.wait_closing(f"{ACTIVE_PANE} .ant-collapse-item .actived")
