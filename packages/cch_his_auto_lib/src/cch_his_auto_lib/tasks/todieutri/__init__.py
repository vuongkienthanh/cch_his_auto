import logging
from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.helper import tracing

URL = "http://emr.ndtp.org/quan-ly-noi-tru/chi-tiet-nguoi-benh-noi-tru/to-dieu-tri"
_logger = logging.getLogger().getChild("todieutri")
_trace = tracing(_logger)


def get_dienbien(driver: Driver) -> str | None:
    try:
        ele = driver.waiting("textarea.dien-bien").text.strip()
        if ele == "":
            return None
        else:
            _logger.info(f"dien bien= {ele}")
            return ele
    except NoSuchElementException:
        _logger.warning("-> can't find dien bien")
        return None


def back(driver: Driver):
    driver.clicking(".footer-btn .right button:nth-child(2)", "go back button")
