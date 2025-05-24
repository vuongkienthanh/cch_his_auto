import logging

from cch_his_auto_lib.driver import get_global_driver
from cch_his_auto_lib.helper import tracing
from cch_his_auto_lib.tasks import search_menu

_lgr = logging.getLogger("bot_indieuduong")
_trace = tracing(_lgr)


def goto(name: str):
    "Open menu *In điều dưỡng*, filter selection based on `name`"
    _d = get_global_driver()
    _d.clicking(".footer-btn .right button:nth-child(3)", "open In điều dưỡng")
    search_menu.goto(name)


from .bangkechiphiBHYT import sign_bangkechiphiBHYT
from .camketchungvenhapvien import get_signature

__all__ = ["sign_bangkechiphiBHYT", "get_signature"]
