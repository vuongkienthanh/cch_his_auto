import logging

from selenium.common import NoSuchElementException


from cch_his_auto.driver import Driver
from . import ACTIVE_PANE

_logger = logging.getLogger().getChild("hosobenhan")

TAB_NUNMBER = 7


def get_bloodtype(driver: Driver) -> str | None:
    try:
        ele = driver.waiting(
            f"{ACTIVE_PANE} tr:nth-child(2) td:nth-child(11)"
        ).text.strip()
        if ele == "":
            return None
        else:
            _logger.info(f"nhommau = {ele}")
            return ele
    except NoSuchElementException:
        _logger.info(" can't find nhommau")
        return None
