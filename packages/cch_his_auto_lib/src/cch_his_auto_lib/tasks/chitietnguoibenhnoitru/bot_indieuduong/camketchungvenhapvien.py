from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import Driver
from . import goto, _logger, _trace


@_trace
def get_signature(driver: Driver) -> str | None:
    main_tab = driver.current_window_handle
    goto(driver, "cam kết chung về nhập viện")
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
