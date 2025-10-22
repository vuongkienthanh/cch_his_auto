import datetime as dt

from selenium.webdriver.remote.webelement import WebElement

from .. import ACTIVE_PANE
from cch_his_auto_lib.driver import Driver


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
        return []
