from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import Driver
from . import ACTIVE_PANE, _logger

TAB_NUMBER = 7
_logger = _logger.getChild("tab_mau")


def get_bloodtype(driver: Driver) -> str | None:
    try:
        ele = driver.waiting(
            f"{ACTIVE_PANE} tr:nth-child(2) td:nth-child(11)"
        ).text.strip()
        if ele == "":
            return None
        else:
            _logger.info(f"bloodtype = {ele}")
            return ele
    except NoSuchElementException:
        _logger.warning("-> can't find bloodtype")
        return None
