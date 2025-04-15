import time
import datetime as dt
import logging

from cch_his_auto.driver import Driver
from . import indieuduong as idd

URL = "http://emr.ndtp.org/quan-ly-noi-tru/chi-tiet-nguoi-benh-noi-tru/"

_logger = logging.getLogger().getChild("chitietnguoibenhnoitru")

def scrape_signature(driver: Driver) -> str | None:
    "try getting signature src of current patient"
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
    except:
        _logger.warning("??? can't find patient signature")
        return None
    finally:
        driver.close()
        driver.switch_to.window(main_tab)
        time.sleep(5)

def get_admission_date(driver: Driver) -> dt.date:
    "Get admission date"
    date = dt.datetime.strptime(
        driver.waiting(
            ".tab-box .content-tab .ant-row .ant-col:nth-child(2) .item-sub b",
            "admission date",
        ).text,
        "%d/%m/%Y %H:%M:%S",
    ).date()
    _logger.debug(f"admisstion_date={date}")
    return date
