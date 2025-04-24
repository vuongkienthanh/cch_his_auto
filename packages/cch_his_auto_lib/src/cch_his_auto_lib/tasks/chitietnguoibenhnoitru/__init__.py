import time
import logging

from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import Driver
from .lower_buttons import indieuduong as idd

URL = "http://emr.ndtp.org/quan-ly-noi-tru/chi-tiet-nguoi-benh-noi-tru/"
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


def scrape_signature(driver: Driver) -> str | None:
    "try getting signature of the current patient"
    _logger.debug("+++ start scrape_signature")
    main_tab = driver.current_window_handle
    idd.open_menu(driver)
    idd.goto(driver, "cam kết chung về nhập viện")
    driver.goto_newtab(main_tab)
    try:
        ele = driver.waiting(".layout-line-item:nth-child(43) img", "patient signature")
        ans = ele.get_dom_attribute("src").strip()
        _logger.info(">>> found patient signature")
        return ans
    except NoSuchElementException:
        _logger.warning("??? can't find patient signature")
        return None
    finally:
        driver.close()
        driver.switch_to.window(main_tab)
        time.sleep(5)
