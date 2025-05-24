import logging

from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import get_global_driver

URL = "http://emr.ndtp.org/quan-ly-noi-tru/chi-tiet-nguoi-benh-noi-tru/"

_lgr = logging.getLogger().getChild("chitietnguoibenhnoitru")

TOP_BTN_CSS = "#root .thong-tin-benh-nhan .bunch-icon"
MAIN_CSS = ".content"
NAV_CSS = f"{MAIN_CSS}>div>div>div>.ant-tabs-nav .ant-tabs-nav-list"
ACTIVE_PANE = f"{MAIN_CSS}>div>div>div>.ant-tabs-tabpane-active"


def is_tab_active(tab: int) -> bool:
    _d = get_global_driver()
    try:
        _d.waiting(
            f"{NAV_CSS}>div:nth-child({tab})[class='ant-tabs-tab ant-tabs-tab-active']"
        )
        return True
    except NoSuchElementException:
        return False


def change_tab(tab: int):
    _d = get_global_driver()
    _d.clicking(f"{NAV_CSS}>div:nth-child({tab})")
    assert is_tab_active(tab)


def wait_patient_page_loaded(ma_hs: int):
    _d = get_global_driver()
    _d.waiting_to_be(
        "#root .patient-information span:nth-child(2) b",
        str(ma_hs),
        "patient id",
    )
