import time
import datetime as dt
import logging

from selenium.common import NoSuchElementException

from cch_his_auto.driver import Driver
from . import indieuduong as idd

URL = "http://emr.ndtp.org/quan-ly-noi-tru/chi-tiet-nguoi-benh-noi-tru/"

_logger = logging.getLogger().getChild("chitietnguoibenhnoitru")


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


def get_admission_date(driver: Driver) -> dt.date:
    ele = driver.waiting(
        ".tab-box .info:nth-child(1) .ant-col:nth-child(2) .item-sub:nth-child(1) b",
        "admission date",
    ).text
    # should exist admission_date
    if ele == "":
        time.sleep(1)
        return get_admission_date(driver)
    date = dt.datetime.strptime(
        ele,
        "%d/%m/%Y %H:%M:%S",
    ).date()
    _logger.debug(f"admisstion_date={date}")
    return date


def get_discharge_date(driver: Driver) -> dt.date | None:
    for _ in range(10):
        time.sleep(1)
        ele = driver.waiting(
            ".tab-box .info:nth-child(3) .ant-col:nth-child(2) .item-sub:nth-child(4) b",
            "discharge date",
        ).text
        if ele != "":
            break
    else:
        _logger.debug("=> can't find discharge_date")
        return None
    date = dt.datetime.strptime(
        ele,
        "%d/%m/%Y %H:%M:%S",
    ).date()
    _logger.debug(f"discharge_date={date}")
    return date


def get_discharge_diagnosis(driver: Driver) -> str | None:
    for _ in range(10):
        time.sleep(1)
        ele = driver.waiting(
            ".tab-box .info:nth-child(3) .ant-col:nth-child(1) .item-sub:nth-child(1) b",
            "discharge diagnosis",
        ).text
        if ele != "":
            break
    else:
        _logger.debug("=> can't find discharge_diagnosis")
        return None
    _logger.debug(f"discharge_diagnosis={ele}")
    return ele


def get_discharge_comorbid(driver: Driver) -> list[str]:
    for _ in range(10):
        time.sleep(1)
        ele = driver.waiting(
            ".tab-box .info:nth-child(3) .ant-col:nth-child(1) .item-sub:nth-child(2) b",
            "discharge comormid",
        ).text
        if ele != "":
            break
    else:
        _logger.debug("=> can't find discharge_comorbid")
        return []
    _logger.debug(f"discharge_comorbid={ele}")
    return ele.split("; ")

def get_discharge_diagnosis_detail(driver: Driver) -> str | None:
    for _ in range(10):
        time.sleep(1)
        ele = driver.waiting(
            ".tab-box .info:nth-child(3) .ant-col:nth-child(1) .item-sub:nth-child(3) b",
            "discharge diagnosis detail",
        ).text
        if ele != "":
            break
    else:
        _logger.debug("=> can't find discharge_diagnosis")
        return None
    _logger.debug(f"discharge_diagnosis_detail={ele}")
    return ele

def get_bloodtype(driver: Driver) -> str | None:
    for _ in range(10):
        time.sleep(1)
        ele = driver.waiting(
            ".tab-box .info:nth-child(1) .ant-col:nth-child(1) .item-sub:nth-child(6) b",
            "bloodtype",
        ).text
        if ele != "":
            break
    else:
        _logger.debug("=> can't find bloodtype")
        return None
    _logger.debug(f"bloodtype={ele}")
    return ele

