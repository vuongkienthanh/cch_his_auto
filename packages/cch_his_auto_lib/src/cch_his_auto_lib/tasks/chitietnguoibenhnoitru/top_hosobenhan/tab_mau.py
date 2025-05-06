from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import Driver
from . import ACTIVE_PANE, _logger

TAB_NUMBER = 7
_logger = _logger.getChild("tab_mau")


def get_bloodtype(driver: Driver) -> str | None:
    for i in range(2, 10):
        try:
            ele = driver.waiting(
                f"{ACTIVE_PANE} tr:nth-child({i}) td:nth-child(12)", "nhóm máu phát"
            ).text.strip()
        except NoSuchElementException:
            _logger.warning("-> can't find bloodtype")
            return None
        else:
            if ele == "Chưa xác định":
                continue
            else:
                _logger.info(f"bloodtype = {ele}")
                return ele
    else:
        _logger.warning("-> can't find bloodtype")
        return None
