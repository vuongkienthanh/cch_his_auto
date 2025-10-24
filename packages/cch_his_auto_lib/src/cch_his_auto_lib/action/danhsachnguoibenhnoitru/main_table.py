from selenium.webdriver.common.keys import Keys

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.action import top_info
from . import _lgr

MAIN_TABLE = "#base-search_component +div .ant-table table tbody"


def search(d: Driver, ma_hs: int):
    _lgr.debug(f"filter_patient ma_hs={ma_hs}")
    ele = d.clear_input(".base-search_component .ant-col:nth-child(2) input")
    ele.send_keys(str(ma_hs))
    ele.send_keys(Keys.ENTER)
    d.wait_closing(f"{MAIN_TABLE} .ant-table-row:nth-child(3)")


def goto_patient(d: Driver, ma_hs: int):
    search(d, ma_hs)
    open_patient(d, 2)


def open_patient(d: Driver, i: int):
    d.clicking2(f"{MAIN_TABLE} tr.ant-table-row:nth-child({i}) td:last-child svg")
    top_info.wait_loaded(d)
