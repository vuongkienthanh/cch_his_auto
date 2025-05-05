import logging

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.helper import tracing
from cch_his_auto_lib.tasks import search_menu

_logger = logging.getLogger("bot_indieuduong")
_trace = tracing(_logger)


def goto(driver: Driver, name: str):
    "Open menu *In điều dưỡng*, filter selection based on `name`"
    driver.clicking(".footer-btn .right button:nth-child(3)", "open In điều dưỡng")
    search_menu.goto(driver, name)


from .bangkechiphiBHYT import sign_bangkechiphiBHYT
from .camketchungvenhapvien import get_signature

__all__ = ["sign_bangkechiphiBHYT", "get_signature"]
