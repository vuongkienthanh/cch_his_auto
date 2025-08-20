import logging

from cch_his_auto_lib.driver import get_global_driver
from cch_his_auto_lib.tracing import tracing
from cch_his_auto_lib.tasks import search_menu

_lgr = logging.getLogger("bot_inbacsi")
_trace = tracing(_lgr)


def goto(name: str):
    "Open menu *In bác sĩ*, filter selection based on `name`"
    _d = get_global_driver()
    _d.clicking(".footer-btn .right button:nth-child(2)", "open In bác sĩ")
    search_menu.goto(name)
