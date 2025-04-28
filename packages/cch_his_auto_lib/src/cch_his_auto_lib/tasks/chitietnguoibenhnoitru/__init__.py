import logging

from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import Driver

URL = "http://emr.ndtp.org/quan-ly-noi-tru/chi-tiet-nguoi-benh-noi-tru/"


TOP_BTN_CSS = "#root .thong-tin-benh-nhan .bunch-icon"

MAIN_CSS = ".content"
NAV_CSS = f"{MAIN_CSS}>div>div>div>.ant-tabs-nav .ant-tabs-nav-list"
ACTIVE_PANE = f"{MAIN_CSS}>div>div>div>.ant-tabs-tabpane-active"

_logger = logging.getLogger().getChild("chitietnguoibenhnoitru")


def is_tab_active(driver: Driver, tab: int) -> bool:
    try:
        driver.waiting(
            f"{NAV_CSS}>div:nth-child({tab})[class='ant-tabs-tab ant-tabs-tab-active']"
        )
        return True
    except NoSuchElementException:
        return False


def change_tab(driver: Driver, tab: int):
    driver.clicking(f"{NAV_CSS}>div:nth-child({tab})")
    assert is_tab_active(driver, tab)


def wait_patient_page_loaded(driver: Driver, ma_hs: int):
    driver.waiting_to_be(
        "#root .patient-information span:nth-child(2) b",
        str(ma_hs),
        "patient id",
    )
