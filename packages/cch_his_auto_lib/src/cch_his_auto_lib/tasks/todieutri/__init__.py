import logging

from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import get_global_driver
from cch_his_auto_lib.tracing import tracing

URL = "http://emr.ndtp.org/quan-ly-noi-tru/chi-tiet-nguoi-benh-noi-tru/to-dieu-tri"

_lgr = logging.getLogger().getChild("todieutri")
_trace = tracing(_lgr)


def get_dienbien() -> str | None:
    _d = get_global_driver()
    try:
        ele = _d.waiting("textarea.dien-bien").text.strip()
        if ele == "":
            return None
        else:
            _lgr.info(f"dien bien= {ele}")
            return ele
    except NoSuchElementException:
        _lgr.warning("-> can't find dien bien")
        return None


def back():
    _d = get_global_driver()
    _d.clicking(".footer-btn .right button:nth-child(2)", "go back button")
