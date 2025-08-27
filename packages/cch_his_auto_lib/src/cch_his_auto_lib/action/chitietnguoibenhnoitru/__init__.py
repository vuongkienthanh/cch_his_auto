import logging

from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import Driver

URL = "http://emr.ndtp.org/quan-ly-noi-tru/chi-tiet-nguoi-benh-noi-tru/"

_lgr = logging.getLogger("chitietnguoibenhnoitru")

TOP_BTN_CSS = "#root .thong-tin-benh-nhan .bunch-icon"
MAIN_CSS = "#root .content"
NAV_CSS = f"{MAIN_CSS} .ant-tabs-nav-list"
ACTIVE_PANE = f"{MAIN_CSS} .ant-tabs-tabpane-active"


def is_tab_active(d: Driver, tab: int) -> bool:
    try:
        d.waiting(f"#rc-tabs-2-panel-{tab}.ant-tabs-tabpane-active")
        return True
    except NoSuchElementException:
        return False


def change_tab(d: Driver, tab: int):
    d.clicking(f"{NAV_CSS}>div[data-node-key='{tab}']")
    assert is_tab_active(d, tab)


def wait_patient_page_loaded(d: Driver, ma_hs: int):
    d.waiting_to_startswith(
        "#root .patient-information span:nth-child(2) b",
        str(ma_hs),
        "patient id",
    )
