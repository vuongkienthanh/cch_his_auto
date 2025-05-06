import logging

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.helper import tracing
from cch_his_auto_lib.tasks import search_menu

_logger = logging.getLogger("bot_inbacsi")
_trace = tracing(_logger)


def goto(driver: Driver, name: str):
    "Open menu *In bác sĩ*, filter selection based on `name`"
    driver.clicking(".footer-btn .right button:nth-child(2)", "open In bác sĩ")
    search_menu.goto(driver, name)
