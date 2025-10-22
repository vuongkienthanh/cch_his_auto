from selenium.common import NoSuchElementException

from . import _lgr
from cch_his_auto_lib.driver import Driver


def dienbien(d: Driver) -> str | None:
    try:
        ele = d.waiting("textarea.dien-bien").text.strip()
        if ele == "":
            return None
        else:
            _lgr.info(f"dien bien= {ele}")
            return ele
    except NoSuchElementException:
        _lgr.warning("-> can't find dien bien")
        return None
