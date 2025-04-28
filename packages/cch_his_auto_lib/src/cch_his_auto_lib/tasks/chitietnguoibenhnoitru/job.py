import time

from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import Driver
from . import bot_indieuduong as idd

from . import _logger


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
